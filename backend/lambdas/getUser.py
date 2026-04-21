import boto3
import json
import datetime
import os

table_name = os.environ['USER_TABLE_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    route_key = event.get('routeKey', '')
    if "GET /get-user" not in route_key:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid endpoint. :(')
        }
    path_params = event.get('pathParameters', {})
    user_email = path_params.get('email')
    if not user_email:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing email.')
        }
    current_time = datetime.datetime.now()
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
        return {
            'statusCode': 200,
            'body': f'Updated timestamp for user {user_email}',
            'user': response
        }
    except Exception as e:
        return {
            'statusCode': 500, 
            'body': "Internal Server Error" + str(e)
        }