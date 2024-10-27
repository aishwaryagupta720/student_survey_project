import psycopg2
import os
import json
import logging
from psycopg2 import OperationalError, InterfaceError, DatabaseError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

db_name = os.environ['DB_NAME']
db_user = os.environ['DB_USER']
db_host = os.environ['DB_HOST']
db_port = os.environ['DB_PORT']
db_password = os.environ['DB_PASSWORD']

def get_db_connection():

    logger.info("Trying to connect to DB")
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        connect_timeout=3
    )
    logger.info("Connection Successful")
    cursor = conn.cursor()
    
    return conn,cursor
    
def execute_query(query, query_params):
    """
    Executes the given query with the provided parameters and returns the result.
    """
    conn, cursor = get_db_connection()

    try:
        cursor.execute(query, query_params)
        result = cursor.fetchall()
        # column_names = [desc[0] for desc in cursor.description]
        # data = [dict(zip(column_names, row)) for row in results]
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
            
            