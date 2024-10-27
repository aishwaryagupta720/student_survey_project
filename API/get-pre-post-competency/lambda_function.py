import json
import logging
import traceback
import psycopg2
from psycopg2 import OperationalError, InterfaceError, DatabaseError
from db_operations import get_db_connection
from get_data_from_id import get_all_questions,get_organization
import collections

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

group_mapping = {
    'First Generation': ['dd5c1e33-8813-46af-9f79-75f10e9d69ff',"%graduate%",'1'],
    'International': ['a54979a3-daed-4b76-8968-663daa743786','International student with non-immigrant (visa) status in the U.S.','0']
}


competencies = ['communication_results','teamwork_results','self_development_results','professionalism_results',
                'leadership_results','critical_thinking_results','technology_results','equity_results',
                'overall_career_readiness_results']

def build_query(request):
    """
    Dynamically builds the SQL query based on the filters provided.
    """
    
    filters = request.get('filters', {})
    
    query_parts = [f"AVG((sr.{competency}->>'result')::float) AS {competency}" for competency in competencies]
    select_statement = ", ".join(query_parts)
    
    query = f"""
        SELECT sr.implementation_time, {select_statement}
        FROM student_response sr
        WHERE 1=1
    """
    query_params=[]
    # WHERE implementation_type IN ('work-exp','course','cohort','work-exp-imex','cohort-imex','course-imex')

    if 'inventory_version' in filters:
        query += " AND sr.inventory_version = %s"
        query_params.append(filters['inventory_version'])
    if 'semester' in filters:
        query += " AND sr.semester = %s"
        query_params.append(filters['semester'])
    if 'org_name' in filters:
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
        query_params=query_params+d_query_params
    
    conditions = """
    GROUP BY sr.implementation_time
    ORDER BY sr.implementation_time;
    """
    query+=conditions
    
    return query,query_params
    


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
            

def transform_data(tuples):
    # Initialize the dictionary with keys as competencies and values as dictionaries with 'pre' and 'post' keys
    result = {competency: {"pre": None, "post": None} for competency in competencies}
    
    for entry in tuples:
        label, *scores = entry
        for score, competency in zip(scores, competencies):
            if label in result[competency]:  # Check if the label is valid for the competency
                score_percentage = ((score-1)/3)*100
                result[competency][label] = score_percentage
            else:
                continue
    
    return result
    
def lambda_handler(event, context):
    
    # data = event.get('body', {})
    data = json.loads(event['body'])
    logger.info(data)

    try:
        query, query_params = build_query(data)
        logger.info(query)
        response = execute_query(query, query_params) 
        structured_scores = transform_data(response)
        logger.info("Final query result: %s", structured_scores)
        

        return {
            'statusCode': 200,
            'body': json.dumps(structured_scores),
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

