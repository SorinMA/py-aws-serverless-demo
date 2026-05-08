import {StrictMode} from "react";
import {createRoot} from "react-dom/client";
import {AuthProvider} from "react-oidc-context";
import {WebStorageStateStore} from "oidc-client-ts";
import App from "./App";
import "./index.css";

const cognitoAuthConfig = {
    authority: import.meta.env.VITE_OIDC_AUTHORITY,
    client_id: import.meta.env.VITE_OIDC_CLIENT_ID,
    redirect_uri: import.meta.env.VITE_OIDC_REDIRECT_URI,
    post_logout_redirect_uri: import.meta.env.VITE_OIDC_POST_LOGOUT_REDIRECT_URI,
    response_type: "code",
    scope: "email openid profile",
    userStore: new WebStorageStateStore({store: window.localStorage})
};

createRoot(document.getElementById("root")!).render(
    <StrictMode>
        <AuthProvider {...cognitoAuthConfig}>
            <App/>
        </AuthProvider>
    </StrictMode>
);