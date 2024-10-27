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

group_mapping = {
    'First Generation': ['dd5c1e33-8813-46af-9f79-75f10e9d69ff',"%graduate%",'1'],
    'International': ['a54979a3-daed-4b76-8968-663daa743786','International student with non-immigrant (visa) status in the U.S.','0']
}


question_ids = ['e13ebf1f-d675-4497-9dee-3cbe2ea4009b','426dee5c-ab40-43a2-a0b7-5fad055074b3']
question_mapping = get_all_questions(question_ids)

def build_query(filters):
    query_params = [list(question_mapping.values())]
    
    query = """
        SELECT 
          item ->> 'question' AS main_question,
          response ->> 'text' AS subquestion,
          response ->> 'response' AS response_value,
          COUNT(*) AS response_count
        FROM 
          student_response AS sr,
          jsonb_array_elements(social_capital) AS item,
          jsonb_array_elements(item -> 'responses') AS response
        WHERE
            item->>'question' ILIKE ANY (%s)
    """
    
    conditions = """
        GROUP BY 
          main_question,
          subquestion,
          response_value
        ORDER BY 
          main_question,
          subquestion,
          response_count DESC;
    """
    
    query_filters,filter_params = build_query_filters(filters)
    
    query+=query_filters
    query+=conditions
    query_params+=filter_params
    
    
    
    
    return query,query_params
    
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


    
def calculate_response(responses):
    question_response_mapping = {}

    for question, category, response, count in responses:
        if question not in question_response_mapping:
            question_response_mapping[question] = {}

        if category not in question_response_mapping[question]:
            question_response_mapping[question][category] = {'responses': {}, 'total': 0}

        # Store responses and counts
        if response not in question_response_mapping[question][category]['responses']:
            question_response_mapping[question][category]['responses'][response] = {'count': 0}
        question_response_mapping[question][category]['responses'][response]['count'] += count
        question_response_mapping[question][category]['total'] += count

    # Calculate percentages
    for question, categories in question_response_mapping.items():
        for category, details in categories.items():
            total = details['total']
            for response, response_details in details['responses'].items():
                count = response_details['count']
                percentage = (count / total) * 100
                response_details['percentage'] = percentage

    return question_response_mapping

def format_output(data):
    output = {}
    for question, categories in data.items():
        output[question] = {}
        for category, details in categories.items():
            responses = []
            counts = []
            percentages = []

            for response, values in details['responses'].items():
                responses.append(response)
                counts.append(values['count'])
                percentages.append(values['percentage'])

            output[question][category] = {
                'values': counts,
                'labels': responses,
                'percentages': percentages
            }

    return output



def lambda_handler(event, context):
    """
    Lambda function handler to process the event and return the filtered result.
    """
    # data = event.get('body', {})
    data = json.loads(event['body'])
    filters = data['filters']

    
    try:
        query, query_params = build_query(filters)
        response = execute_query(query, query_params)
        
        question_response_mapping = calculate_response(response)
        output= format_output(question_response_mapping)
        
        logger.info(output)
        
        return {
            'statusCode': 200,
            'body': json.dumps(output),
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

