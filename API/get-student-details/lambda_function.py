import json
import logging
import traceback
import psycopg2
from psycopg2 import OperationalError, InterfaceError, DatabaseError
from db_operations import get_db_connection
from get_data_from_id import get_all_students,get_all_questions,get_organization
import datetime

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

question_ids = ['e11392e3-f30e-43ba-ad39-8d6cb6de6a6d','d9b64530-72b3-45b2-b714-2016c5ac7626','c974a276-95a6-4237-869e-5161234da62d']
work_questions = ['e11392e3-f30e-43ba-ad39-8d6cb6de6a6d']
supervisor_questions = ['f18fd226-42fa-4a69-a27b-a4cf03d4abf1','c68d6ddd-829b-49fd-9f15-a09b7e4b3399']

def get_observers(filter_params):
    
    query = """
        SELECT
            (question.element->>'order') AS question_order,
            array_agg(response.element->>'response') AS responses
        FROM 
            student_response sr,
            jsonb_array_elements(sr.work_experience) AS question(element)
            CROSS JOIN jsonb_array_elements(question.element->'responses') AS response(element)
        WHERE 
            (question.element->>'order')::int IN (59, 60)
            AND sr.email = %s 
            AND sr.implementation_type = %s 
            AND sr.use_case_id = %s 
            AND sr.semester = %s 
            AND (response.element->>'response' IS NOT NULL)
        GROUP BY question_order;
    """
    filter_params.pop()
    responses = execute_query(query, filter_params)
    logger.info(responses)
    if responses:
        for response in responses:
            if len(responses)>1 and response == responses[1]:
                output={
                'Evaluator 2 Name':response[1][0]+" "+response[1][1],
                'Evaluator 2 Email':response[1][2]
                }
            output={
                'Evaluator Name':response[1][0]+" "+response[1][1],
                'Evaluator Email':response[1][2]
                }
            
    else:
        output={}
    
    return output

def get_student_data(data):
    
    email,name,last_name,org = get_all_students(data['id'])
    part = {'Name':name+' '+last_name,'Organisation':org,'Email':email}
    implementation_type = data['implementation_type']
    use_case,semester = data['filter'].split(":")
    question_mapping = get_all_questions(question_ids)
    questions = ['%'+question+'%' for question in list(question_mapping.values())]
    logger.info(questions)
    
    demo_query = """
        SELECT
            sr.timestamp,
            jsonb_agg(jsonb_build_object('question', elem->>'question', 'response', elem->>'response')) AS questions_responses
        FROM
            student_response sr,
            jsonb_array_elements(sr.demographics) AS elem
        WHERE
            sr.email = %s AND
            sr.implementation_type = %s AND
            sr.use_case_id = %s AND
            sr.semester = %s AND
            elem->>'question' ILIKE ANY (%s)
        GROUP BY
            sr.timestamp
        ORDER BY sr.timestamp DESC
    """
    work_query = """
        SELECT
            sr.timestamp,
            jsonb_agg(jsonb_build_object('question', elem->>'question', 'response', elem->>'response')) AS questions_responses
        FROM
            student_response sr,
            jsonb_array_elements(sr.work_experience) AS elem
        WHERE
            email = %s AND implementation_type = %s AND use_case_id = %s AND semester = %s AND
            elem->>'question' ILIKE ANY (%s)
        GROUP BY sr.timestamp 
        ORDER BY sr.timestamp DESC
    """
    
    # query+= """ 
    #     GROUP BY demo->>'question',work->>'question',demo->>'response',work->>'response'
    #      """
    
    query_params = [email,implementation_type,use_case,semester,questions]
    
        
    return demo_query,work_query,query_params,part

def format_details(demo,work):
        
    result = {}
    latest_timestamp = datetime.datetime.min 
    
    for data in [demo,work]:
        if not data:
            continue
        entry = data[0]
        timestamp = entry[0]  # assuming timestamp is always the second item
        questions = entry[1]  # assuming questions are always the third item
        
        if timestamp > latest_timestamp:
            # Update the latest timestamp and reset the result dictionary
            latest_timestamp = timestamp
        
        for item in questions:
                question = item['question'].lower()  # Convert to lower case to simplify matching
                response = item['response']
                if 'degree' in question:
                    result['degree'] = response
                elif 'program' in question:
                    result['program'] = response
                elif 'experiential learning' in question:
                    result['work_experience'] = response
                    
    result['timestamp']= latest_timestamp.strftime('%Y-%m-%d %H:%M:%S')

    return result
    

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

    try:
        demo_query,work_query, query_params,part = get_student_data(data)
        demo_result = execute_query(demo_query, query_params)
        work_result = execute_query(work_query, query_params)
        observer_result = get_observers(query_params)
        logger.info("Final query result: %s", demo_result)
        logger.info("Final query result: %s", work_result)
        
        output = format_details(demo_result,work_result)
        
        output.update(part)
        output.update(observer_result)
        

        return {
            'statusCode': 200,
            'body': json.dumps(output)
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