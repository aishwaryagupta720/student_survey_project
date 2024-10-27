import os
import boto3
import traceback
from botocore.exceptions import ClientError

def write_to_db(data):
    table_name = os.environ.get('TABLE_NAME')
    
    if not table_name:
        raise ValueError("DynamoDB table name is not configured.")
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    try:
        # Insert the item into DynamoDB
        response = table.put_item(Item=data)
        return response
        
    except ClientError as e:
        print(f"Failed to write data to DynamoDB: {e}")
        traceback.print_exc()  #  standard error
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        traceback.print_exc()
        raise

