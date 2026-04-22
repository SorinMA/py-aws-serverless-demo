import boto3
import json
import datetime
import os
import re
import logging

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

table_name = os.environ['USER_TABLE_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    route_key = event.get('routeKey', '')
    if "GET /get-user" not in route_key:
        logger.warning(f'Invalid route key: {route_key}')
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps('Invalid endpoint. :(')
        }
    path_params = event.get('pathParameters', {})
    user_email = path_params.get('email')
    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not user_email:
        logger.warning('Email parameter missing')
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Email is required'})
        }

    if not re.match(email_pattern, user_email) or len(user_email) > 254:
        logger.warning(f'Invalid email format: {user_email}')
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Invalid email format'})
        }
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
            ReturnValues="UPDATED_NEW"
        )
        logger.info(f'Successfully updated user: {user_email}')
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'message': f'Updated timestamp for user {user_email}',
                'updatedAttributes': response.get('Attributes', {})
            }, default=str)
        }
    except Exception as e:
        logger.error(f'Error updating user {user_email}: {str(e)}', exc_info=True)
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': 'Internal Server Error',
                'message': str(e)
            })
        }