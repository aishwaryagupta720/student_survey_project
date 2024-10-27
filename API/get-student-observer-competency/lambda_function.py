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

observer_question_mapping={
    'communication' : {
        5:'Oral Communication',
        6:'Written Communication' ,
        7:'Non-verbal Communication',
        8:'Active Listening'
    },
    'teamwork' : {
        10:'Build Relationships for Collaboration',
        11:'Respect Diverse Perspectives',
        12:'Integrate Strengths'
    },
    'self_development' : {
        14:'Awareness of Strengths & Challenges',
        15:'Professional Development',
        16:'Networking'
    },
    'professionalism' : {
        18:'Act With Integrity',
        19:'Demonstrate Dependability',
        20:'Achieve Goals'
    },
    'leadership' : {
        22:'Inspire, Persuade, & Motivate',
        23:'Engage Various Resources & Seek Feedback',
        24:'Facilitate Group Dynamics'
    },
    'critical_thinking' : {
        26:'Display Situational Awareness',
        27:'Gather & Analyze Data',
        28:'Make Effective & Fair Decisions'
    },
    'technology' : {
        30:'Leverage Technology',
        31:'Adapt to New Technologies',
        32:'Use Technology Ethically'
    },
    'equity' : {
        34:'Engage Multiple Perspectives',
        35:'Use Inclusive & Equitable Practices',
        36:'Advocate'
    }
}
                
def get_observers(query_filter,filter_params):
    
    query = """
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
    
    query+=query_filter
    response = execute_query(query, filter_params)
    return response
    
def build_observer_query(emails):
    """
    Dynamically builds the SQL query based on the filters provided.
    """
    
    email_string = ', '.join(f"'{email}'" for email in emails)
    query_parts = [f"AVG((sr.{competency}->>'result')::float) AS {competency}" for competency in competencies]
    select_statement = ", ".join(query_parts)

    query = f"""
        SELECT {select_statement}
        FROM observer_response sr
        WHERE email IN ({email_string})
    """
    
    return query

def questions_query(filter_query,query_params,emails):
    """
    Dynamically builds the SQL query based on the filters provided.
    """
        
    student_parts = []
    observer_parts = []
    union_params = []
    email_string = ', '.join(f"'{email}'" for email in emails)
    for comp in question_mapping:
        student_part = f"""
        SELECT 
            '{comp}' AS competency,
            elements->>'order' AS question_order,
            AVG((elements->>'score_value')::float) AS score_values
        FROM 
            student_response sr,
            jsonb_array_elements(sr.{comp}) AS elements
        WHERE 1=1
        """
        
        observer_part = f"""
        SELECT 
            '{comp}' AS competency,
            elements->>'order' AS question_order,
            AVG((elements->>'score_value')::float) AS score_values
        FROM 
            observer_response sr,
            jsonb_array_elements(sr.{comp}) AS elements
        """
        
        
        student_part +=filter_query
        student_part+=""" 
        GROUP BY question_order
            """
        observer_part +=f"""
         WHERE email IN ({email_string})
        """
        observer_part +=""" 
        GROUP BY question_order
            """     
        
        student_parts.append(student_part)
        observer_parts.append(observer_part)
        union_params+=query_params
        
    final_student_query = " UNION ALL ".join(student_parts)
    # final_student_query+="""
    # ORDER BY question_order
    # """
    
    final_observer_query = " UNION ALL ".join(observer_parts)
    # final_observer_query +="""
    # ORDER BY question_order
    # """
    logger.info(final_student_query)
    logger.info(final_observer_query)
    
    return final_student_query,union_params,final_observer_query

def build_query(request):
    """
    Dynamically builds the SQL query based on the filters provided.
    """
    
    filters = request.get('filters', {})
    
    query_parts = [f"AVG((sr.{competency}->>'result')::float) AS {competency}" for competency in competencies]
    select_statement = ", ".join(query_parts)
    
    query = f"""
        SELECT {select_statement}
        FROM student_response sr
        WHERE implementation_type IN ('work-exp','course','cohort','work-exp-imex','cohort-imex','course-imex')
        AND implementation_time IN ('post')
    """
    
    query_filters=""
    query_params=[]
    

    if 'inventory_version' in filters:
        query_filters += " AND sr.inventory_version = %s"
        query_params.append(filters['inventory_version'])
    if 'semester' in filters:
        query_filters += " AND sr.semester = %s"
        query_params.append(filters['semester'])
    if 'org_name' in filters:
        org = get_organization(filters['org_name'])
        query_filters += " AND sr.org_name = %s"
        query_params.append(org)
    # if 'implementation_type' in filters:
    #     query += " AND sr.implementation_type = %s"
    #     query_params.append(filters['implementation_type'])
    if 'use_case_id' in filters:
        query_filters += " AND sr.use_case_id = %s"
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
        query_filters+=d_query
        query_params=query_params+d_query_params
        
    query+=query_filters
    
    emails = get_observers(query_filters,query_params)
    emails = [email[0] for email in emails]
    observer_query = build_observer_query(emails)
    
    student_questions,questions_params,observer_questions = questions_query(query_filters,query_params,emails)

    
    return query,query_params,observer_query,student_questions,questions_params,observer_questions
    


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
            

def transform_data(student,evaluator):
    
    labeled_student = [dict(zip(competencies, row)) for row in student][0]
    labeled_evaluator = [dict(zip(competencies, row)) for row in evaluator][0]

    logger.info(labeled_evaluator)
    result = {competency: {"student": None, "evaluator": None} for competency in competencies}
    
    for competency in competencies:
        if competency in labeled_student: 
            score_percentage = ((labeled_student[competency]-1)/3)*100
            result[competency]["student"] = score_percentage
        if competency in labeled_evaluator: 
            score_percentage = ((labeled_evaluator[competency]-1)/3)*100
            result[competency]["evaluator"] = score_percentage
    
    return result

def transform_questions(student,evaluator):
    output = {key:{value:{} for value in question_mapping[key].values()} for key in question_mapping}
    
    for cat,order,value in student:
        order = question_mapping[cat][int(order)]
        score_percentage = ((value-1)/3)*100
        output[cat][order]['student']=score_percentage
        
    for cat,order,value in evaluator:
        order = observer_question_mapping[cat][int(order)]
        score_percentage = ((value-1)/3)*100
        output[cat][order]['evaluator']=score_percentage
    
    logger.info(output)
    return output
        
    
    
def lambda_handler(event, context):
    
    # data = event.get('body', {})
    data = json.loads(event['body'])
    logger.info(data)
    if 'implementation_type' in data['filters'] and data['filters']['implementation_type']!='work-exp':
        return {
            'statusCode': 200,
            'body': json.dumps({}),
            'headers': {
                'Content-Type': 'application/json'
            }
        } 
    try:
        query, query_params,observer_query,student_questions,questions_params,observer_questions = build_query(data)
        student_response = execute_query(query, query_params) 
        observer_response = execute_query(observer_query, []) 
        student_questions_response = execute_query(student_questions, questions_params) 
        observer_questions_response = execute_query(observer_questions, []) 
        structured_scores = transform_data(student_response,observer_response)
        logger.info("Final query result: %s", structured_scores)
        questions = transform_questions(student_questions_response,observer_questions_response)
        # logger.info("student_questions_response query result: %s", student_questions_response)
        # logger.info("observer_questions_response query result: %s", observer_questions_response)
        
        structured_scores.update(questions)

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

