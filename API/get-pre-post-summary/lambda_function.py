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
            COUNT(DISTINCT CASE WHEN sr.implementation_time = 'pre' THEN sr.response_id ELSE NULL END) AS total_student_responses_pre,
            COUNT(DISTINCT CASE WHEN sr.implementation_time = 'post' THEN sr.response_id ELSE NULL END) AS total_student_responses_post,
            AVG(sr.duration) AS average_duration
        FROM student_response sr
        WHERE 1=1
    """
    
    weekly_query = """
        SELECT 
            COUNT(DISTINCT CASE WHEN sr.implementation_time = 'pre' THEN sr.response_id ELSE NULL END) AS total_student_responses_pre,
            COUNT(DISTINCT CASE WHEN sr.implementation_time = 'post' THEN sr.response_id ELSE NULL END) AS total_student_responses_post,
            AVG(sr.duration) AS average_duration,
            TO_CHAR(DATE_TRUNC('week', sr.timestamp), 'YYYY-MM-DD') AS period
        FROM student_response sr
        WHERE 1=1
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
    weekly_query+=filter_query
    
    if 'demographics_question' in filters and filters['demographics_question']!=[]:
        d_query, d_query_params = handle_demographics_filtering(filters['demographics_question'])
    
        query+=d_query
        weekly_query+=d_query
        query_params=query_params+d_query_params
        
    weekly_query+= """
            AND sr.timestamp >= NOW() - INTERVAL '14 days'
        GROUP BY DATE_TRUNC('week', sr.timestamp)
        ORDER BY period
        LIMIT 2
    """
    
    return query, weekly_query, query_params,org_logo


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

def get_comparisons(weekly_result):
    # Get today's date and the start of the current week (Monday)
    period_start=None
    today = date.today()
    current_week_start = today - timedelta(days=today.weekday())  # Monday of the current week
    previous_week_start = current_week_start - timedelta(days=7) 
    
    if len(weekly_result)==0:
        return [0,0,0]
    elif len(weekly_result)==1:
        data = weekly_result[0]
        if parse_period(data[3])>= current_week_start:
            return [100,100,100]
        else:
            return [-100,-100,-100]
    else:
        current_data = list(weekly_result[1][:3])
        prev_data = list(weekly_result[0][:3])

        result = []
        for current,prev in zip(current_data,prev_data) :
            if int(prev) == 0:
                if int(current) != 0:
                    result.append(100.0)
                else:
                    result.append(0.0)  
            else:
                percentage_change = ((float(current) - float(prev)) / float(prev)) * 100
                result.append(round(percentage_change, 2))
            
            logger.info(percentage_change)
            logger.info(current)
            logger.info(prev)
        return result

        


def lambda_handler(event, context):
    """
    Lambda function handler to process the event and return the filtered result.
    """
    # data = event.get('body', {})
    data = json.loads(event['body'])
    logger.info(data)
    filters = data['filters']
    
    try:
        query, weekly_query, query_params,logo = build_query(filters)

        result = execute_query(query, query_params)[0]
        weekly_result = execute_query(weekly_query, query_params)
        
        
        logger.info("Final query result: %s", result)
        logger.info("weekly query result: %s", weekly_result)
        
        comparison = get_comparisons(weekly_result)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'logo' : logo,
                'pre': [str(result[0]),str(comparison[0])],
                'post': [str(result[1]),str(comparison[1])],
                'average_duration': [str(result[2]),str(comparison[2])]
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
