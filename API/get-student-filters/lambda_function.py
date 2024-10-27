import json
import logging
import traceback
import psycopg2
from psycopg2 import OperationalError, InterfaceError, DatabaseError
from db_operations import get_db_connection
from get_data_from_id import get_all_students,get_organization

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_distinct_values(id):
    
    email = get_all_students(id)
    
    filter_query = """SELECT 
                        implementation_type,
                        use_case_id,
                        semester
                    FROM 
                        student_response
                    WHERE
                        email = %s 
                    GROUP BY 
                        implementation_type, use_case_id, semester;
                    """

        
    return filter_query,[email]

def filter_dropdown(result):
    output = {value[0]:[value[1]+":"+value[2]] for value in result}
    return output
    

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
    id = data['id']

    try:
        query, query_params = get_distinct_values(id)
        result = execute_query(query, query_params)
        logger.info("Final query result: %s", result)
        
        output = filter_dropdown(result)
        

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