import json
import re

DEFAULT_HEADERS = {"Content-Type": "application/json"}
_EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

def json_response(status_code: int, body, headers=None):
    merged = dict(DEFAULT_HEADERS)
    if headers:
        merged.update(headers)
    return {
        "statusCode": status_code,
        "headers": merged,
        "body": json.dumps(body),
    }

def is_valid_email(email: str) -> bool:
    if not email or len(email) > 254:
        return False
    return _EMAIL_PATTERN.match(email) is not None