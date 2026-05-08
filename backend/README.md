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
```

- **403 Forbidden**
  - Make sure you are sending the **API key value** (not the key name) in `x-api-key`.
  - Make sure you send exactly one `Authorization` header:
    - `Authorization: Bearer <IdToken>`
  - In Postman, avoid setting the token in both the **Authorization** tab and the **Headers** tab at the same time (can cause duplicate headers).

- **401 Unauthorized**
  - Usually means the JWT is missing/invalid/expired, or you are using the wrong token type.
  - Use `AuthenticationResult.IdToken`.

### If you receive a `NEW_PASSWORD_REQUIRED` challenge

If the user was created with a **temporary password**, the `InitiateAuth` response may NOT contain `AuthenticationResult`.  
Instead, it will contain:

- `ChallengeName: "NEW_PASSWORD_REQUIRED"`
- `Session: "<...>"`

In that case, you must respond to the challenge once to set a new password.

#### RespondToAuthChallenge (set a new password)

**Request**

- **Method:** `POST`
- **URL:** `https://cognito-idp.eu-north-1.amazonaws.com/`

**Headers**

- `Content-Type: application/x-amz-json-1.1`
- `X-Amz-Target: AWSCognitoIdentityProviderService.RespondToAuthChallenge`

**Body (raw JSON)**

```json
{
  "ClientId": "<CognitoUserPoolClientId>",
  "ChallengeName": "NEW_PASSWORD_REQUIRED",
  "Session": "<Session-from-InitiateAuth>",
  "ChallengeResponses": {
    "USERNAME": "test@example.com",
    "NEW_PASSWORD": "YourNewPassword123!"
  }
}
```


## Pre-deploy check to validate the PostConfirmationLambdaFunction
1. Run: `serverless package --stage userStage`

2. Check: `.serverless/cloudformation-template-update-stack.json`
