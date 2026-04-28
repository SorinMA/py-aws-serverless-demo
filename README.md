# py-aws-serverless-demo

A demonstration project showcasing AWS serverless architecture using the Serverless Framework with Python Lambda functions.

## Project Structure

- **backend/** - Serverless API with Lambda functions, DynamoDB, S3, and Cognito (User Pool)
- **frontend/** - Static React (Vite) app deployed to S3 + CloudFront (Serverless Framework)

## Tech Stack

- **AWS Lambda** - Python 3.12 runtime
- **API Gateway** - REST API endpoints
- **DynamoDB** - NoSQL database with Global Secondary Indexes
- **S3** - Object storage + static website hosting
- **CloudFront** - CDN for frontend
- **Cognito User Pool** - Authentication
- **Serverless Framework** - Infrastructure as Code

## Deploy order (important)

For a **fresh setup** or after running `serverless remove` on both services, deploy in this order:

1) Frontend first (it exports CloudFront values used by the backend)
2) Backend second