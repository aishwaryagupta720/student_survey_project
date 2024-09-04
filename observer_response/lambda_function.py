import json
import logging
import boto3
import re
import traceback
from process_json import process_all_data
from queries import write_to_db

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# initialise user data dictionary
user_data={}



def lambda_handler(event, context):
    data = json.loads(event['body'])
    logger.info("Processing the observer input data")
    # logger.info(data)
    
    # validate outcomes
    valid_pdf_report = any(outcome['title'] == "PDF Report" for outcome in data['outcomes'])
    if not valid_pdf_report:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps("Response Invalid")
        }
    
    try:
        user_data = process_all_data(data)
        logger.info(user_data)
        
        result = write_to_db(user_data)
        print("Data inserted successfully:", result)
    
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg + f" At line: {traceback.format_exc()}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(f"An error occurred: {e}")
        }

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps("Data was processed successfully.")
    }
