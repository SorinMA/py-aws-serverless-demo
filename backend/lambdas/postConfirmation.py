import os
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb")

def _get_display_name(user_attributes: dict) -> str:
    """
    Cognito may store name in different attributes depending on your signup UI.
    Standard attributes to consider:
      - name
      - given_name + family_name
      - preferred_username
    """
    name = (user_attributes.get("name") or "").strip()
    if name:
        return name

    given = (user_attributes.get("given_name") or "").strip()
    family = (user_attributes.get("family_name") or "").strip()
    full = " ".join([p for p in [given, family] if p]).strip()
    if full:
        return full

    return (user_attributes.get("preferred_username") or "").strip()

def lambda_handler(event, context):
    """
    Cognito Post Confirmation trigger.
    Docs: Cognito invokes this after the user is confirmed.
    Important: you MUST return the event back to Cognito.

    event.request.userAttributes contains user attributes like:
      - email
      - sub (Cognito user id)
      - email_verified
      - etc.
    """
    table_name = os.environ["USER_TABLE_NAME"]
    table = dynamodb.Table(table_name)

    user_attrs = (event.get("request") or {}).get("userAttributes") or {}

    # Use email as the DynamoDB partition key (matches your table schema).
    email = (user_attrs.get("email") or "").strip().lower()
    if not email:
        # No email => nothing to store; do not break the Cognito flow.
        return event

    name = _get_display_name(user_attrs)
    now = datetime.now(timezone.utc).isoformat()

    item = {
        "email": email,
        "name": name,
        "updatedDate": now,
        # Helpful to store; stable unique identifier in Cognito
        "cognitoSub": user_attrs.get("sub", ""),
    }

    try:
        table.put_item(
            Item=item,
            ConditionExpression="attribute_not_exists(email)",
        )
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code")
        if code == "ConditionalCheckFailedException":
            # User already exists in DynamoDB -> ignore.
            return event
        # Unexpected DynamoDB error: raise so it's visible in CloudWatch logs.
        raise

    return event