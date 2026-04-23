# Backend API

Serverless user management API built with AWS Lambda, DynamoDB, and API Gateway (REST API).

## Stack

- **Runtime:** Python 3.12 (AWS Lambda)
- **API Gateway:** REST API
- **Auth:** API Key + Cognito User Pool (JWT)
- **Database:** DynamoDB (GSIs: `name`, `name + updatedDate`)
- **Storage:** S3 (bucket provisioned; endpoints TBD)
- **Region:** `eu-north-1`

---

## Endpoints

### `GET /get-user/{email}`

Updates the user `updatedDate` field in DynamoDB and returns a confirmation response.

#### Required headers

- `x-api-key: <api-key-value>`
- `Authorization: Bearer <id-token>`

---

## Testing Authentication (Cognito) with Postman

This project uses a Cognito **User Pool App Client** (no secret) and the `USER_PASSWORD_AUTH` flow to obtain tokens.

### 1) Get a JWT (IdToken)

**Request**

- **Method:** `POST`
- **URL:** `https://cognito-idp.eu-north-1.amazonaws.com/`

**Headers**

- `Content-Type: application/x-amz-json-1.1`
- `X-Amz-Target: AWSCognitoIdentityProviderService.InitiateAuth`

**Body (raw JSON)**

```json
{
  "AuthFlow": "USER_PASSWORD_AUTH",
  "ClientId": "<CognitoUserPoolClientId>",
  "AuthParameters": {
    "USERNAME": "test@example.com",
    "PASSWORD": "YourPassword123"
  }
}