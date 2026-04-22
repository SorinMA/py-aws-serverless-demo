import boto3
import datetime
import os
import logging
from .common import json_response, is_valid_email

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

table_name = os.environ['USER_TABLE_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    path_params = event.get('pathParameters', {})
    user_email = path_params.get('email')
    # Validate email format
    if not user_email:
        logger.warning('Email parameter missing')
        return json_response(400, {'error': 'Email is required'})

    if not is_valid_email(user_email):
        logger.warning(f'Invalid email format: {user_email}')
        return json_response(400, {'error': 'Invalid email format'})
    current_time = datetime.datetime.utcnow().isoformat() # enforce ISO 8601 format
    try:
        response = table.update_item(
            Key={'email': user_email}, 
            UpdateExpression="SET #u = :t",
            ExpressionAttributeNames={
                "#u": "updatedDate" 
            },
            ExpressionAttributeValues={
                ":t": str(current_time)
            },
            ConditionExpression="attribute_exists(email)", # Prevent accidental user creation on update_item
            ReturnValues="UPDATED_NEW"
        )
        logger.info(f'Successfully updated user: {user_email}')
        return json_response(200, {
            'message': f'Updated timestamp for user {user_email}',
            'updatedAttributes': response.get('Attributes', {})
        })
    except Exception as e:
        logger.error(f'Error updating user {user_email}: {str(e)}', exc_info=True)
        return json_response(500, {
            'error': 'Internal Server Error :('
        })
