import json
import logging
import traceback
import psycopg2
from db_operations import execute_query,get_db_connection
from psycopg2 import OperationalError, InterfaceError, DatabaseError


# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_organization():
    """
    Fetches all questions from the question_bank based on the provided IDs.
    """
    query = """
    SELECT org_name,organization_id
    FROM organization_record;
    """
    
    conn, cursor = get_db_connection()
    try:
        cursor.execute(query)
        responses = cursor.fetchall()
        mapping = {}
        for response in responses:
            mapping[response[0]] = response[1]
        logger.info(mapping)
        return mapping
    
        
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

    try:
        org = get_organization()
        
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
        
    return {
            'statusCode': 200,
            'body': json.dumps(org),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
