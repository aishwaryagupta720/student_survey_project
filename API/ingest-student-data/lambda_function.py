import json
import logging
import boto3
import re
import traceback
from transform_json import process_all_data
from query_rds import write_to_rds , read_from_rds
from update_organisation import check_organisation

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # for internal test only 
    # data = event['body']
    # logger.info(data)
    # query_response = write_to_rds(data)
    # logger.info("Data inserted successfully:", query_response)
    
    
    data = json.loads(event['body'])
    logger.info("Processing the input data")
    logger.info(data)
    try:
        valid_pdf_report = any(outcome['title'] == "PDF Report" for outcome in data['outcomes'])
        if not valid_pdf_report:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps("Response Invalid")
            }
        
        results = process_all_data(data)
        logger.info(results)
        
        if results['use_case_id']!='testing':
            insert_query_response = write_to_rds(results)
            print("Data inserted successfully:", insert_query_response)
            
        org_query_response = check_organisation(results)
        print("Org updated successfully:", org_query_response)
        

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