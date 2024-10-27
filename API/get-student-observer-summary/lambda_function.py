import json
import logging
import traceback
import psycopg2
from datetime import datetime, timedelta, date
from psycopg2 import OperationalError, InterfaceError, DatabaseError
from db_operations import get_db_connection
from get_data_from_id import get_all_questions,get_organization

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

group_mapping = {
    'First Generation': ['dd5c1e33-8813-46af-9f79-75f10e9d69ff',"%graduate%",'1'],
    'International': ['a54979a3-daed-4b76-8968-663daa743786','International student with non-immigrant (visa) status in the U.S.','0']
}

def parse_period(period_str):
        return datetime.strptime(period_str, '%Y-%m-%d').date()
        
def build_query(filters):
    """
    Dynamically builds the SQL query based on the filters provided.
    """
    query = """
        SELECT 
            COUNT(DISTINCT CASE WHEN sr.implementation_time = 'post' THEN sr.response_id ELSE NULL END) AS total_student_responses_post,
            AVG(sr.duration) AS average_duration
        FROM student_response sr
        WHERE 1=1
    """
    
    evaluator_query = """
        SELECT
            response.element->>'response' AS response_value
        FROM 
            student_response sr,
            jsonb_array_elements(sr.work_experience) AS question(element)
            CROSS JOIN jsonb_array_elements(question.element->'responses') AS response(element)
        WHERE 
            (question.element->>'order')::int IN (59, 60) -- change with question id from question_bank
            AND (response.element->>'text' = 'Email')
            AND (response.element->>'response' IS NOT NULL)
        """
    
    query_params = []
    org_logo=''
    filter_query =""
    
    if 'inventory_version' in filters:
        filter_query += " AND sr.inventory_version = %s"
        query_params.append(filters['inventory_version'])
    if 'semester' in filters:
        filter_query += " AND sr.semester = %s"
        query_params.append(filters['semester'])
    if 'org_name' in filters:
        org,org_logo = get_organization(filters['org_name'])
        filter_query += " AND sr.org_name = %s"
        query_params.append(org)
    if 'implementation_type' in filters:
        filter_query += " AND sr.implementation_type = %s"
        query_params.append(filters['implementation_type'])
    if 'use_case_id' in filters:
        filter_query += " AND sr.use_case_id = %s"
        query_params.append(filters['use_case_id'])
    if 'implementation_time' in filters:
        filter_query += " AND sr.implementation_time = %s"
        query_params.append(filters['implementation_time'])
    if 'demographic_group' in filters:
        demographic_group = filters['demographic_group']
        if 'demographics_question' not in filters:
            filters['demographics_question']=[]
        filters['demographics_question'].append({
            "question": group_mapping[demographic_group][0],
            "response": group_mapping[demographic_group][1],
            "condition": group_mapping[demographic_group][2]
        })
    
    query +=filter_query
    evaluator_query+=filter_query
    
    if 'demographics_question' in filters and filters['demographics_question']:
        d_query, d_query_params = handle_demographics_filtering(filters['demographics_question'])
    
        query+=d_query
        evaluator_query+=d_query
        query_params=query_params+d_query_params
        
    # weekly_query+= """
    #         AND sr.timestamp >= NOW() - INTERVAL '14 days'
    #     GROUP BY DATE_TRUNC('week', sr.timestamp)
    #     ORDER BY period
    #     LIMIT 2
    # """
    
    return query, evaluator_query, query_params,org_logo

def get_eval_count(emails):
    emails = [email[0] for email in emails]
    email_string = ', '.join(f"'{email}'" for email in emails)
    query = f"""
        SELECT 
            COUNT(DISTINCT sr.response_id) 
        FROM observer_response sr
        WHERE email IN ({email_string})
    """
    results = execute_query(query, [])
    counts = [result[0] for result in results]
    return counts[0]

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


def execute_query(query, query_params):
    """
    Executes the given query with the provided parameters and returns the result.
    """
    conn, cursor = get_db_connection()

    try:
        cursor.execute(query, query_params)
        result = cursor.fetchall()
        return result
    except (OperationalError, InterfaceError, DatabaseError) as db_error:
        logger.error("Database error occurred:", exc_info=db_error)
        raise Exception(db_error)
    except Exception as e:
        logger.error("An unexpected error occurred:", exc_info=e)
        raise Exception(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

        


def lambda_handler(event, context):
    """
    Lambda function handler to process the event and return the filtered result.
    """
    # data = event.get('body', {})
    data = json.loads(event['body'])
    logger.info(data)
    filters = data['filters']
    
    try:
        query, email_query, query_params,logo = build_query(filters)

        result = execute_query(query, query_params)[0]
        emails = execute_query(email_query, query_params)
        
        logger.info("Student query result: %s", result)
        logger.info("Observer query result: %s", emails)
        
        if len(emails)>0:
            evaluators = get_eval_count(emails)
        else:
            evaluators = 0
        logger.info("Observer query result: %s", evaluators)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'logo' : logo,
                'student': str(result[0]),
                'evaluator': evaluators,
                'average_duration': str(result[1])
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
