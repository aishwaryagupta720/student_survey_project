import json
import logging
import traceback
import psycopg2
from psycopg2 import OperationalError, InterfaceError, DatabaseError
from db_operations import execute_query
from get_data_from_id import get_all_questions,get_organization
import collections
from collections import Counter

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def build_query(filters):
    work_query = """
        SELECT 
            elements->>'response' AS response
        FROM 
            student_response sr,
            jsonb_array_elements(sr.work_experience) AS elements
        WHERE 
            (elements->>'order')::int = 61  
    """
    time_query = """
        SELECT
            hours.value->>'response' AS hours_response,
            weeks.value->>'response' AS weeks_response,
            pay.value->>'response' AS pay_response,
            credit.value->>'response' AS credit_response
            
        FROM
            student_response sr,
            jsonb_array_elements(sr.work_experience) AS elements,
            jsonb_array_elements(elements->'responses') WITH ORDINALITY AS hours(value, index),
            jsonb_array_elements(elements->'responses') WITH ORDINALITY AS weeks(value, index),
            jsonb_array_elements(elements->'responses') WITH ORDINALITY AS pay(value, index),
            jsonb_array_elements(elements->'responses') WITH ORDINALITY AS credit(value, index)
        WHERE
            (elements->>'order')::int = 62
            AND hours.index = 1  
            AND weeks.index = 2  
            AND pay.index = 3  
            AND credit.index = 4 
    """
    
    query_filters,query_params = build_query_filters(filters)
    
    work_query+=query_filters
    time_query+=query_filters
    
    return work_query,time_query,query_params
    
def build_query_filters(filters):
    """
    Dynamically builds the SQL query to fetch a specific question response from a JSONB column
    based on provided filters.
    """
    # Initialize the base part of the query
    query = """ 
    """
    # Initialize query parameters list starting with the 'order' number
    query_params = []

    # Dynamically add other conditions based on the filters dictionary
    if 'inventory_version' in filters:
        query += " AND sr.inventory_version = %s"
        query_params.append(filters['inventory_version'])
    
    if 'semester' in filters:
        query += " AND sr.semester = %s"
        query_params.append(filters['semester'])
    
    if 'org_name' in filters:
        # Assuming get_organization() returns a cleaned or validated organization identifier
        org = get_organization(filters['org_name'])
        query += " AND sr.org_name = %s"
        query_params.append(org)
    
    if 'implementation_type' in filters:
        query += " AND sr.implementation_type = %s"
        query_params.append(filters['implementation_type'])
    
    if 'use_case_id' in filters:
        query += " AND sr.use_case_id = %s"
        query_params.append(filters['use_case_id'])
    
    if 'demographic_group' in filters:
        demographic_group = filters['demographic_group']
        if 'demographics_question' not in filters:
            filters['demographics_question']=[]
        filters['demographics_question'].append({
            "question": group_mapping[demographic_group][0],
            "response": group_mapping[demographic_group][1],
            "condition": group_mapping[demographic_group][2]
        })
    
    if 'demographics_question' in filters and filters['demographics_question']:
        d_query, d_query_params = handle_demographics_filtering(filters['demographics_question'])
    
        query+=d_query
        query_params+=d_query_params

    return query, query_params

def handle_demographics_filtering(demographics_questions):
    """
    Adds filtering conditions for demographics questions.
    """
    keys = [filter['question'] for filter in demographics_questions]
    
    mapping = get_all_questions(keys)
    query = """
    AND EXISTS (
        SELECT 1
        FROM jsonb_array_elements(sr.demographics) AS elem
        WHERE 
    """
    query_params = []
    conditions = []
    for demog in demographics_questions:
        operator = 'ILIKE' if demog['condition'] == '0' else 'NOT ILIKE'
        conditions.append(f"(elem->>'question' ILIKE %s AND elem->>'response' {operator} %s)")
        query_params.append(mapping[demog['question']])
        query_params.append(demog['response'])
    query += " AND ".join(conditions) + ")"
    
    return query, query_params

def calculate_percentage(responses):
    """
    Calculates the percentage of each unique response in the total responses.
    """
    response_counts = {key: 0 for key in responses}  
    for response in responses:
        if response in response_counts:
            response_counts[response] += 1 
            
    total_responses = len(responses)
    response_percentages = {response: (count / total_responses) * 100 for response, count in response_counts.items()}
    
    return {
        'keys' : list(response_percentages.keys()),
        'percentage' :  list(response_percentages.values()),
        'counts' : list(response_counts.values())
    }
    
def calculate_stats(data):
        total = len(data) 
        filtered_data = [int(x) for x in data if x is not None]
        if len(filtered_data)>0:
            minimum = min(filtered_data)
            maximum = max(filtered_data)
            average = sum(filtered_data) / len(filtered_data)
        else:
            minimum = maximum = average = 0
        return {
            'min': minimum,
            'max': maximum,
            'avg': average,
            'response': (len(filtered_data)/total)*100
        }
        
def organize_data(responses):
    """
    Organizes data from a list of tuples into separate lists based on their indices.
    """
    hours = []
    weeks = []
    paid = []
    credit = []
    
    for response in responses:
        hours.append(response[0]) 
        weeks.append(response[1]) 
        paid.append(response[2])   
        credit.append(response[3]) 
    
    
    paid.sort()
    credit.sort()
    
    hours_stats = calculate_stats(hours)
    weeks_stats = calculate_stats(weeks)
    paid_stats = calculate_percentage(paid)
    credit_stats = calculate_percentage(credit)
    
    
    return hours_stats,weeks_stats,paid_stats,credit_stats
        
    

def lambda_handler(event, context):
    """
    Lambda function handler to process the event and return the filtered result.
    """
    # data = event.get('body', {})
    data = json.loads(event['body'])
    logger.info(data['filters'])
    filters = data['filters']
    if 'implementation_type' not in filters or filters['implementation_type']!="work-exp":
        return {
            'statusCode': 200,
            'body': json.dumps({}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    
    try:
        work_query,time_query, query_params = build_query(filters)

        work_result = execute_query(work_query, query_params)
        time_result = execute_query(time_query, query_params)
        
        work_result = [work[0] for work in work_result]
        work = calculate_percentage(work_result)
        logger.info(work)
        
        hours,weeks,paid,credit = organize_data(time_result)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                            "Experiential Learning Type": {
                                "type" : "pie",
                                "percentages":work['percentage'],
                                "labels" :work['keys'],
                                "values" :work['counts']
                            },
                            "Pay Status": {
                                "type" : "pie",
                                "percentages":paid['percentage'],
                                "labels" :paid['keys'],
                                "values" :paid['counts']
                            },
                            "Academic Credit": {
                                "type" : "pie",
                                "percentages":credit['percentage'],
                                "labels" :credit['keys'],
                                "values" :credit['counts']
                            },
                            "Average Hours and Weeks": {
                                "type" : "table",
                                "hours":hours,
                                "weeks" :weeks
                            }
                        }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    except Exception as e:
        logger.error("Error processing request: %s", e, exc_info=True)  # Logs stack trace with the error

        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
