import json
import logging
import traceback
import psycopg2
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

demographic_mapping = { 
    'Gender': 'd61f96be-29e6-4a26-bf62-55993bb6b8ac',
    'DemographicCategory': 'a54979a3-daed-4b76-8968-663daa743786',
    'PresetGroups': 'dd5c1e33-8813-46af-9f79-75f10e9d69ff',
    'Disability': '9a149e36-a5e8-4602-b6a4-e47aab952508',
    'LGBTQ': 'bd7e349a-4e0a-435d-9a68-551cc7999981',
    'Language': 'd16579f7-ec39-4c00-b8e9-4b297a62c10d',
    'Parent': '37963d7a-dd81-4366-9ec0-5e02b0dadf63',
    'Military': 'af505188-1f22-405c-88e0-d953591f0a6b',
    'Caregiver': 'c2436b4e-8084-4346-b78e-372b063aa9d4',
    'FinanceSources': 'ba35d9d9-8265-4e8e-8bc5-49264505917c',
    'Age': 'a7dab9b7-a07d-430c-a8c7-3113f12d2c00',
    'Program': 'd9b64530-72b3-45b2-b714-2016c5ac7626',
    'AcademicLevel': 'c974a276-95a6-4237-869e-5161234da62d'
}


def get_distinct_values(request):
    filter_query=""
    type = request.get('type', '')
    dropdown_field = request.get('dropdown', '')
    filters = request.get('filters', {})
    params = []
    
    if type == "demographics":
        if len(dropdown_field) > 0:
            question_ids = demographic_mapping[dropdown_field]
            mapping = get_all_questions([question_ids])
            question=mapping[question_ids]
            logger.info(question)
            

            # Start building query to get distinct responses for this specific question
            filter_query = """
                SELECT DISTINCT elem->>'response' AS response
                FROM student_response sr, jsonb_array_elements(sr.demographics) AS elem
                WHERE elem->>'question' ILIKE %s
            """
            params.append('%'+question+'%')
                
                
        

    else:
        filter_query = f"SELECT DISTINCT sr.{dropdown_field} FROM student_response sr WHERE 1=1"

    
   

    if 'inventory_version' in filters:
        filter_query += " AND sr.inventory_version ILIKE %s"
        params.append(filters['inventory_version'])
    if 'semester' in filters:
        filter_query += " AND sr.semester ILIKE %s"
        params.append(filters['semester'])
    if 'org_name' in filters:
        org = get_organization(filters['org_name'])
        filter_query += " AND sr.org_name ILIKE %s"
        params.append(org)
    if 'implementation_type' in filters:
        filter_query += " AND sr.implementation_type ILIKE %s"
        params.append('%'+filters['implementation_type']+'%')
    if 'use_case_id' in filters:
        filter_query += " AND sr.use_case_id ILIKE %s"
        params.append(filters['use_case_id'])
    if 'demographic_group' in filters:
        demographic_group = filters['demographic_group']
        if 'demographics_question' not in filters:
            filters['demographics_question']=[]
        filters['demographics_question'].append({
            "question": group_mapping[demographic_group][0],
            "response": group_mapping[demographic_group][1],
            "condition": group_mapping[demographic_group][2]
        })
        
        
        params.append(filters['use_case_id'])

    if 'demographics_question' in filters and filters['demographics_question']!=[]:
        logger.info(filters['demographics_question'])
        d_query, d_query_params = handle_demographics_filtering(type,filters['demographics_question'])

        filter_query+=d_query
        params+=d_query_params
        
    return filter_query,params

    

def handle_demographics_filtering(type,demographics_questions):
    """
    Adds filtering conditions for demographics questions.
    """
    keys = [filter['question'] for filter in demographics_questions]
    query=""
    mapping = get_all_questions(keys)
    if type=="field":
        query = """
        AND EXISTS (
            SELECT 1
            FROM jsonb_array_elements(sr.demographics) AS elem
            WHERE 
        """
    else:
         query = """
         """
         
    query_params = []
    conditions = []
    for demog in demographics_questions:
        operator = 'ILIKE' if demog['condition'] == '0' else 'NOT '
        conditions.append(f"(elem->>'question' ILIKE %s AND elem->>'response' {operator} %s)")
        query_params.append('%'+mapping[demog['question']]+'%')
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

def make_predefined_groups(request, groups):
    output = []
    options = [ "High School","None of the above (College experience outside the US, etc.)","Prefer not to respond","Some College","Unknown"]
    if any(option in groups for option in options):
        output.append('First Generation')
    
    request['dropdown'] = 'Category'
    query,params = get_distinct_values(request)
    result = execute_query(query, params)
    logger.info("Final query result: %s", result)
    categories = [item[0] for item in result]
        
    if 'International student with non-immigrant (visa) status in the U.S.' in categories:
        output.append('International')
    
    return output

def lambda_handler(event, context):
    """
    Lambda function handler to process the event and return the filtered result.
    """
    # data = event.get('body', {})
    data = json.loads(event['body'])
    logger.info(data)

    try:
        query, query_params = get_distinct_values(data)

        logger.info("Final query: %s", query)

        result = execute_query(query, query_params)
        logger.info("Final query result: %s", result)
        result_list = [item[0] for item in result if item[0]!=None]

        dropdown_field = data.get('dropdown', '')

        if len(result_list)>0:

            if dropdown_field=='implementation_type':
                result_list = [result for result in result_list if "-imex" not in result]

            if dropdown_field=='Group':
                result_list = make_predefined_groups(data,result_list)
        
            return {
                'statusCode': 200,
                'body': json.dumps(sorted(result_list))
                }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps([])
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