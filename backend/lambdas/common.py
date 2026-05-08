import json
import re
import os

DEFAULT_HEADERS = {"Content-Type": "application/json"}
_EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

def json_response(status_code, body):
    origin = os.environ.get("CORS_ALLOW_ORIGIN")
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Headers": "Authorization,Content-Type,X-Api-Key",
        "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
    }
    if origin:
        headers["Access-Control-Allow-Origin"] = origin
    return {
        "statusCode": status_code,
        "headers": headers,
        "body": json.dumps(body),
    }

def is_valid_email(email: str) -> bool:
    if not email or len(email) > 254:
        return False
    return _EMAIL_PATTERN.match(email) is not None