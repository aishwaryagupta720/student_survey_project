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
    
    if 'demographics_question' in filters and filters['demographics_question']:
        d_query, d_params = handle_demographics_filtering(filters['demographics_question'])
    
        filter_query+=d_query
        query_params+=d_params
        
    query_parts = []
    union_params = []
    for comp in competencies:
        part = f"""
        SELECT 
            '{comp}' AS competency,
            elements->>'order' AS question_order,
            array_agg(elements->>'score_value') AS score_values
        FROM 
            student_response sr,
            jsonb_array_elements(sr.{comp}) AS elements
        """
        part+=filter_query
        part+=""" 
        GROUP BY question_order
            """
        query_parts.append(part)
        union_params+=query_params
        
    final_query = " UNION ALL ".join(query_parts)
    final_query+="""
    ORDER BY question_order
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
    formatted_result = {key:{} for key in competencies}
    for row in response:
        index = question_mapping[row[0]].get(int(row[1]))
        formatted_result.get(row[0],{}).update({ index : row[2] })
        
    return formatted_result
        
    
    
def categorize_scores_by_order(data):
    score_labels = {
        '1.0':'Emerging Knowledge',
        '2.0':'Understanding',
        '3.0':'Early Application',
        '4.0':'Advanced Application'
    }
    results = {}
    
    for order, scores in data.items():
        for i in range(len(scores)):
            if scores[i] == '5.0':
                scores[i] = '1.0'
        
        results[order] = {label: 0 for label in score_labels.values()}
        results[order]["Total"] = 0  # Initialize total count for this question order
        results[order]["Max"] = [0,""]
    
    
    # Categorize scores and count entries and calculate %
    for order, scores in data.items():
        for score in scores:
            label = score_labels.get(score, "Undefined")  # Handle undefined scores 
            results[order][label]+=1
            results[order]["Total"] += 1
        for label in results[order]:
            if label not in ["Total","Max"]:
                if results[order]["Total"]!=0:
                    results[order][label] = [round((results[order][label]/results[order]["Total"])*100,2),results[order][label]]
                else:
                    results[order][label] = [0,results[order][label]]
                    
                if results[order][label][0]>results[order]['Max'][0]:
                    results[order]['Max'][0]=results[order][label][0]
                    results[order]['Max'][1]=label

    return results


def lambda_handler(event, context):
    
    # data = event.get('body', {})
    data = json.loads(event['body'])
    logger.info(data)
    
    try:
        query, query_params = build_query(data)
        result = execute_query(query, query_params) 
        logger.info(query)
        formatted_result=format_response(result)
        logger.info(formatted_result)
        
        for category,data in formatted_result.items():
            formatted_result[category] = categorize_scores_by_order(data)
        
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

