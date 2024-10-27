import json
import logging
import traceback
import psycopg2
from psycopg2 import OperationalError, InterfaceError, DatabaseError
from db_operations import get_db_connection

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_all_students(id):
    """
    Fetches all questions from the question_bank based on the provided IDs.
    """
    query = """
    SELECT email
    FROM student_record
    WHERE id = %s;
    """
    mapping ={}
    conn, cursor = get_db_connection()
    try:
        logger.info(id)
        cursor.execute(query, (id,))
        response = cursor.fetchone()

        
        return response[0]
    
        
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
            
def get_all_questions(question_ids):
    """
    Fetches all questions from the question_bank based on the provided IDs.
    """
    query = """
    SELECT id, question
    FROM question_bank
    WHERE id = ANY(%s::UUID[]);
    """
    mapping ={}
    conn, cursor = get_db_connection()
    try:
        logger.info(question_ids)
        cursor.execute(query, (question_ids,))
        response = cursor.fetchall()

        for q_tuple in response:
            mapping[q_tuple[0]] = q_tuple[1]
        
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

def get_organization(org_id):
    """
    Fetches all questions from the question_bank based on the provided IDs.
    """
    query = """
    SELECT org_name
    FROM organization_record
    WHERE organization_id = %s;
    """
    
    conn, cursor = get_db_connection()
    try:
        cursor.execute(query, (org_id,))
        response = cursor.fetchall()
        logger.info(response)
        return response[0]
    
        
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