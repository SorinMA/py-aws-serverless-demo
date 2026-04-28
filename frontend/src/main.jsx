import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { AuthProvider } from "react-oidc-context";
import './index.css'
import App from './App.jsx'

const cognitoAuthConfig = {
  authority: "https://cognito-idp.eu-north-1.amazonaws.com/eu-north-1_SEsuwO4XV",
  client_id: "7omb93dm674444e9s5mlkcrjai",
  redirect_uri: "https://d2hrj96483he4t.cloudfront.net/auth/callback",
  response_type: "code",
  scope: "email openid profile",
};

// https://d2hrj96483he4t.cloudfront.net/

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider {...cognitoAuthConfig}>
      <App />
    </AuthProvider>
  </StrictMode>,
)