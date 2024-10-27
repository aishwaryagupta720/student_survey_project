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

question_ids = ['bce1b03e-0ebe-4251-b223-ede97fa5b0a0',
                '0f70338f-8652-4be3-b917-dddfdcb035b9','045cfb38-02dd-44da-b49f-4e72619568c2','2d9c4098-bdcd-45c3-a59b-8d03e73507a7',
                'b79e4cf4-01ca-4a2d-b34b-7c5fec535215']



def build_query(filters):
    
    question_mapping = get_all_questions(question_ids)
    questions = list(question_mapping.values())
    questions_string = ['%'+q+'%' for q in questions]
    query = """
        SELECT
            elem->>'question' AS question,
            elem->>'response' AS response,
            COUNT(*) AS response_count
        FROM
            student_response sr,
            jsonb_array_elements(sr.career_mobility) AS elem
        WHERE
            elem->>'question' ILIKE ANY (%s)
    """
    
    order= """ 
        GROUP BY elem->>'question',elem->>'response'
        ORDER BY elem->>'question' ,elem->>'question'
         """
    
    query_params = [questions_string]
    
    filter_query,filter_params = build_query_filters(filters)
    
    query = query+filter_query+order
    query_params+=filter_params
    
    return query,query_params
    
def build_query_filters(filters):
    """
    Dynamically builds the SQL query to fetch a specific question response from a JSONB column
    based on provided filters.
    """
    query = """ 
    """
    query_params = []

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
        
    if 'demographics_question' in filters and filters['demographics_question']!=[]:
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
        query_params.append("%"+mapping[demog['question']]+"%")
        query_params.append("%"+demog['response']+"%")
    query += " AND ".join(conditions) + ")"
    
    return query, query_params
    
def calculate_response(response):
    question_response_mapping = {}

    for question, response, count in response:
        if question not in question_response_mapping:
            question_response_mapping[question] = {'responses': {}, 'total': 0}
        
        question_response_mapping[question]['responses'][response] = {'count': count }
        question_response_mapping[question]['total'] += count
    
    for question, details in question_response_mapping.items():
        total = details['total']
        for response in details['responses']:
            count = details['responses'][response]['count']
            percentage = (count / total) * 100
            details['responses'][response]['percentage'] = percentage
        
    return question_response_mapping

def format_output(data):
    output = {}
    for question in data:
        responses =[]
        counts=[]
        percentages=[]
        for response,values in data[question]['responses'].items():
            responses.append(response)
            counts.append(values['count'])
            percentages.append(values['percentage'])
        output[question]={
        'values':counts ,
        'labels' :responses ,
        'percentages' : percentages, 
        }

    return output
    
    
def lambda_handler(event, context):
    # data = event.get('body', {})
    data = json.loads(event['body'])
    filters = data['filters']
    logger.info(data)
    
    try:
        
        query, query_params = build_query(filters)
        result = execute_query(query, query_params) 

        question_response_mapping = calculate_response(result)
        logger.info("Final query : %s", question_response_mapping)
        output= format_output(question_response_mapping)

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
