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
org_table = os.environ['ORG_TABLE']

def connect_db():

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
    

def write_to_rds(data):
    conn=None
    cursor=None
    try:
        conn,cursor=connect_db()
        
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
    
def get_org(org_id):
    
    try:
        conn,cursor=connect_db()
        
        sql = f"SELECT * FROM {org_table} WHERE org_name = %s"
        logger.info(sql)
    
        cursor.execute(sql, (org_id,))
        result = cursor.fetchone()
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
    
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


    if result:
        data = dict(zip(columns, result))
        return data, True
    else:
        return {}, False
    
def create_org(data):
    conn=None
    cursor=None
    try:
        conn, cursor = connect_db()

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {org_table} ({columns}) VALUES ({placeholders})"
        logger.info(sql)
        data_tuple = tuple(data.values())
        
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

def update_org(data):
    conn = None
    cursor = None
    try:
        conn, cursor = connect_db()
        
        # Prepare the SET part of the SQL statement
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        # Create the SQL update statement
        sql = f"UPDATE {table_name} SET {set_clause} WHERE condition_column = %s"
        logger.info(sql)
        
        # Prepare the data tuple
        data_tuple = tuple(data.values()) + (condition_value,)
    
        # Execute the SQL statement
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
        conn,cursor=connect_db()
        
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

