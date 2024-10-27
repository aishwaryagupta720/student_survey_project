import json
from db_operations import get_db_connection ,execute_query
import logging
from psycopg2 import OperationalError, InterfaceError, DatabaseError
import psycopg2
import boto3
from contextlib import closing
from datetime import datetime

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# AWS S3 Configuration
S3_BUCKET = 'cri-db-backup'
timestamp = datetime.now().strftime('%Y-%m-%d-%H')
S3_KEY = f'student_response/db_dump_{timestamp}.json'


def lambda_handler(event, context):
    # Connect to the database
    with closing(get_db_connection()) as conn, conn.cursor() as cursor:
        # Execute a query
        cursor.execute("SELECT row_to_json(t) FROM (SELECT * FROM student_response) t;")
        records = cursor.fetchall()
        
        # Convert records to a list of dictionaries
        data = [record[0] for record in records]
        logger.info("Got the data")
        # Write data to S3
        s3 = boto3.client('s3')
        s3.put_object(Bucket=S3_BUCKET, Key=S3_KEY, Body=json.dumps(data))
        
        return {
            'statusCode': 200,
            'body': json.dumps('Data successfully written to S3.')
        }


# def lambda_handler(event, context):
#     # question_data = {
#     #     "target": ["students"],  # array of strings
#     #     "question_order": 61,
#     #     "category": "Work Experience",
#     #     "org_name": "NACE",
#     #     "question": "Which best describes your current or most recent experiential learning opportunity?",
#     #     "options": [
#     #         {"option": "Internship", "score": 1},
#     #         {"option": "Co-op", "score": 2},
#     #         {"option": "Practicum experience (e.g., nursing, student teaching, or other clinical experience)", "score": 3},
#     #         {"option": "Micro-internship", "score": 4},
#     #         {"option": "Externship", "score": 5},
#     #         {"option": "On-campus student work", "score": 6},
#     #         {"option": "Apprenticeship", "score": 7},
#     #         {"option": "Job Shadowing", "score": 8},
#     #         {"option": "Faculty-led research projects", "score": 9},
#     #         {"option": "Classroom based projects", "score": 10},
#     #         {"option": "Other (please specify:)", "score": 11},
#     #         {"option": "N/A", "score": 12},
#     #     ]
#     # }
#     question_data = {
#         "target": ["students"],  # array of strings
#         "question_order": 60,
#         "category": "Work Experience",
#         "org_name": "NACE",
#         "question": "Evaluator #2's Contact Information:",
#         "options": [
#               {
#               "question":"First Name"
#           },
#           {
#               "question":"Last Name"
#           },
#           {
#               "question":"Email"
#           }
#         ]
#     }
#     try:
#         # Insert query
#         query = """
#             INSERT INTO question_bank ( target, question_order, category, org_name, question, options)
#             VALUES (%s, %s, %s, %s, %s, %s)
#         """
#         query_params = [
#             question_data["target"],  # JSON encode arrays for PostgreSQL
#             question_data["question_order"],
#             question_data["category"],
#             question_data["org_name"],
#             question_data["question"],
#             json.dumps(question_data["options"])  # JSON encode the options
#         ]
#         # Execute query with parameters
#         result = execute_query(query, query_params)
        
        
#     except (OperationalError, InterfaceError, DatabaseError) as db_error:
#         logger.error("Database error occurred:", exc_info=db_error)
#         raise Exception(db_error)
#     except Exception as e:
#         logger.error("An unexpected error occurred:", exc_info=e)
#         raise Exception(e)

#     return {
#         'statusCode': 200,
#         'body': result
#     }


