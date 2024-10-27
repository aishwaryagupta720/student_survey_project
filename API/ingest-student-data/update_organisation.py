import json
import logging
import boto3
import re
import traceback
from query_rds import get_org , create_org


# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def check_organisation(data):
    
    try:
    
        org_data,org_exists = get_org(data['org_name'])
        
        if org_exists:
            logger.info(org_data)
                
        
        else:
            logger.info("Creating Organisation")
            org_keys = ['org_name','email', 'org_type','implementation_type','inventory_version','use_case_id','semester']
            
            filtered_dict = {key: data[key] for key in org_keys if key in data}
            filtered_dict['implementation_type']=[].append(filtered_dict['implementation_type'])
            filtered_dict['inventory_version']=[filtered_dict['inventory_version']]
            filtered_dict['email']=filtered_dict['email'].split('@')[1]
            filtered_dict['org_name'] = filtered_dict['org_name'].strip()
    
            response = create_org(filtered_dict)
            return response
            
    except KeyError as e:
        error_msg = f"Missing key error: {str(e)} - Check data structure and ensure all keys are present."
        logger.error(error_msg + f" At line: {traceback.format_exc()}")
        raise Exception(error_msg)
    except ValueError as e:
        error_msg = f"Value error: {str(e)} - Check data types of fields."
        logger.error(error_msg + f" At line: {traceback.format_exc()}")
        raise Exception(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg + f" At line: {traceback.format_exc()}")
        raise Exception(error_msg)

        
        