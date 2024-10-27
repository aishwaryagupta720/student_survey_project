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

question_mapping={
    'communication' : {
        4:'Oral Communication',
        5:'Written Communication' ,
        6:'Non-verbal Communication',
        7:'Active Listening'
    },
    'teamwork' : {
        9:'Build Relationships for Collaboration',
        10:'Respect Diverse Perspectives',
        11:'Integrate Strengths'
    },
    'self_development' : {
        13:'Awareness of Strengths & Challenges',
        14:'Professional Development',
        15:'Networking'
    },
    'professionalism' : {
        17:'Act With Integrity',
        18:'Demonstrate Dependability',
        19:'Achieve Goals'
    },
    'leadership' : {
        21:'Inspire, Persuade, & Motivate',
        22:'Engage Various Resources & Seek Feedback',
        23:'Facilitate Group Dynamics'
    },
    'critical_thinking' : {
        25:'Display Situational Awareness',
        26:'Gather & Analyze Data',
        27:'Make Effective & Fair Decisions'
    },
    'technology' : {
        29:'Leverage Technology',
        30:'Adapt to New Technologies',
        31:'Use Technology Ethically'
    },
    'equity' : {
        33:'Engage Multiple Perspectives',
        34:'Use Inclusive & Equitable Practices',
        35:'Advocate'
    }
}

competencies = list(question_mapping.keys())

def build_query(request):
    """
    Dynamically builds the SQL query based on the filters provided.
    """
    
    filters = request.get('filters', {})
    
    filter_query = """
    WHERE
        1=1
    """

    query_params=[]
    

    if 'inventory_version' in filters:
        if filters['inventory_version']!="":
            filter_query += " AND sr.inventory_version = %s"
            query_params.append(filters['inventory_version'])
    if 'semester' in filters:
        if filters['semester']!="":
            filter_query += " AND sr.semester = %s"
            query_params.append(filters['semester'])
    if 'org_name' in filters:
        if filters['org_name']!="":
            org = get_organization(filters['org_name'])
            filter_query += " AND sr.org_name = %s"
            query_params.append(org)
    if 'implementation_type' in filters:
        if filters['implementation_type']!="":
            filter_query += " AND sr.implementation_type = %s"
            query_params.append(filters['implementation_type'])
    if 'use_case_id' in filters:
        if filters['filters']!="":
            filter_query += " AND sr.use_case_id = %s"
            query_params.append(filters['use_case_id'])
    if 'implementation_time' in filters:
        if filters['implementation_time']!="":
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
    
    if 'demographics_question' in filters and filters['demographics_question']!=[]:
        d_query, d_params = handle_demographics_filtering(filters['demographics_question'])
    
        filter_query+=d_query
        query_params+=d_params
        
    query_parts = []
    union_params = []
    for comp in competencies:
        part = f"""
        SELECT 
            '{comp}' AS competency,
            implementation_time,
            elements->>'order' AS question_order,
            AVG((elements->>'score_value')::float) AS score_values
        FROM 
            student_response sr,
            jsonb_array_elements(sr.{comp}) AS elements
        """
        part+=filter_query
        part+=""" 
        GROUP BY question_order,implementation_time
            """
        query_parts.append(part)
        union_params+=query_params
        
    final_query = " UNION ALL ".join(query_parts)
    final_query+="""
    ORDER BY question_order,implementation_time
    """
    # logger.info(final_query)
    
    return final_query,union_params
    


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
    
def format_response(response):
    formatted_result = {key: {} for key in question_mapping}
    
    for row in response:
        competency, implementation_time, order, score = row
        order = int(order)  
        
        if implementation_time not in ['pre', 'post']:
            continue  

        if competency in question_mapping and order in question_mapping[competency]:
            question_name = question_mapping[competency][order]
        else:
            question_name = f"Unknown Question {order}"
        
        if question_name not in formatted_result[competency]:
            formatted_result[competency][question_name] = []
            
        score_percentage = ((score-1)/3)*100
        
        formatted_result[competency][question_name].append({
            implementation_time : score_percentage
        })
        
    return formatted_result


def lambda_handler(event, context):
    
    # data = event.get('body', {})
    data = json.loads(event['body'])
    logger.info(data)
    
    try:
        query, query_params = build_query(data)
        result = execute_query(query, query_params) 
        formatted_result = format_response(result)
        
        logger.info("Final query result: %s", formatted_result)


        return {
            'statusCode': 200,
            'body': json.dumps(formatted_result),
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

