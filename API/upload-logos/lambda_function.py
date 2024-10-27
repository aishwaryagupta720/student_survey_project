import json
import boto3
import os
from db_operations import get_db_connection
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

# def lambda_handler(event, context):
#     bucket_name = 'cri-organization-logos'
#     folder_names = event['orgs']

#     for folder_name in folder_names:
#         s3.put_object(Bucket=bucket_name, Key=folder_name + '/logo/')

#     return {
#         'statusCode': 200,
#         'body': 'Folders created successfully!'
#     }

def lambda_handler(event, context):
    
    bucket_name = "cri-organization-logos"
    path_template = "{org_id}/logo/logo.png"
    
    conn,cursor = get_db_connection()
    try:
        # for org_id in event['orgs']:
        #         logo_url = f"https://{bucket_name}.s3.amazonaws.com/{path_template.format(org_id=org_id)}/logo/logo.png"
        #         # logo_url = f"s3://{bucket_name}/{path_template.format(org_id=org_id)}"
        #         update_query = """
        #             UPDATE organization_record
        #             SET logo_url = %s
        #             WHERE organization_id = %s
        #         """
        #         cursor.execute(update_query, ('NULL', org_id))
        #         conn.commit()
        #         print(f"Updated logo URL for org ID: {org_id}")
        uni = ['Saint Martin&#x27;s University','Saint Martin&amp;#x27;s University']
        update_query = """
            UPDATE student_response 
            SET org_name = REPLACE(org_name, '&#x27;', "'");
            """
        update_query_2 = """
            UPDATE student_response 
            SET org_name = REPLACE(org_name, '&amp;#x27;', "'");
        """
        cursor.execute(update_query)
        cursor.execute(update_query_2)
        conn.commit()
    except Exception as e:
        logger.error("An unexpected error occurred:", exc_info=e)
        raise Exception(e)
    
    
