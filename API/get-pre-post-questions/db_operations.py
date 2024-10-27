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