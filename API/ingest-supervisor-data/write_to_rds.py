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
        logger.error("OperationalError occurred:", oe)
        raise Exception(oe)

    except InterfaceError as ie:
        logger.error("InterfaceError occurred:", ie)
        raise Exception(ie)

    except DatabaseError as de:
        logger.error("DatabaseError occurred:", de)
        raise Exception(de)

    except Exception as e:
        logger.error("An unexpected error occurred:", e)
        raise Exception(e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


    return {
        'statusCode': 200,
        'body': json.dumps('Data successfully inserted into the database')
    }

def read_from_rds():
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
        
        sql = f"SELECT * FROM {table_name}"
        cursor.execute(sql)
        
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        conn.commit()
    except OperationalError as oe:
        logger.error("OperationalError occurred:", oe)
        raise Exception(oe)

    except InterfaceError as ie:
        logger.error("InterfaceError occurred:", ie)
        raise Exception(ie)

    except DatabaseError as de:
        logger.error("DatabaseError occurred:", de)
        raise Exception(de)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

