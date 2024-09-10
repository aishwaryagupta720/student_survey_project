import json
import logging
import boto3
import re
import traceback
from transform_json import process_all_data
from write_to_rds import write_to_rds

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # print(type(event))
    # data = json.loads(event['body'])
    
    data = event['body']

    logger.info("Processing the input data")
    logger.info(data)
    
    # validate outcomes
    valid_pdf_report = any(outcome['title'] == "PDF Report" for outcome in data['outcomes'])
    if not valid_pdf_report:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps("Response Invalid")
        }
    
    try:
        # custom_fields = process_custom_fields(data['custom_fields'])
        # logger.info(custom_fields)
        
        results = process_all_data(data)
        logger.info(results)
        
        query_response = write_to_rds(results)

        print("Data inserted successfully:", query_response)
    
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
            'body': json.dumps("Response recorded successfully.")
        }