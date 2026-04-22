# Backend API

Serverless user management API built with AWS Lambda, DynamoDB, and API Gateway.

## Stack

- **Python 3.12** on AWS Lambda
- **DynamoDB** with GSI indexes (name, name+updatedDate)
- **S3** for file storage
- **Region**: eu-north-1

## API

### GET /get-user/{email}
Updates user timestamp and returns confirmation.