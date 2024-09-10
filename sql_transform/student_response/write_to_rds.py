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
table_name = os.environ['TABLE_NAME']
db_password = os.environ['DB_PASSWORD']

def write_to_rds(data):
    conn=None
    cursor=None
    try:
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
        
        columns = ', '.join(data.keys())  
        placeholders = ', '.join(['%s'] * len(data))  
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        logger.info(sql)
        # Prepare the data tuple, converting dictionaries and lists to JSON strings
        data_tuple = tuple(json.dumps(value) if isinstance(value, (dict, list)) else value for value in data.values())


        cursor.execute(sql, data_tuple)
        conn.commit()
    except OperationalError as oe:
        print("OperationalError occurred:", oe)

    except InterfaceError as ie:
        print("InterfaceError occurred:", ie)

    except DatabaseError as de:
        print("DatabaseError occurred:", de)

    except Exception as e:
        print("An unexpected error occurred:", e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


    return {
        'statusCode': 200,
        'body': json.dumps('Data successfully inserted into the database')
    }

