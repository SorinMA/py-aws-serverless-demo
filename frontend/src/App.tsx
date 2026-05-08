import {useState} from "react";
import {useAuth} from "react-oidc-context";
import "./App.css";
import {getUser, type GetUserResponse} from "./api/backend";

function App() {
    const auth = useAuth();

    const [result, setResult] = useState<GetUserResponse | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [isCallingApi, setIsCallingApi] = useState(false);

    const onCallGetUser = async () => {
        setError(null);
        setResult(null);

        const accessToken = auth.user?.id_token;
        const email = auth.user?.profile?.email as string | undefined;

        if (!accessToken) {
            setError("Missing access token (not authenticated).");
            return;
        }
        if (!email) {
            setError("No email claim found in the user profile.");
            return;
        }

        try {
            setIsCallingApi(true);
            const data = await getUser({email, accessToken});
            setResult(data);
        } catch (e) {
            setError(e instanceof Error ? e.message : String(e));
        } finally {
            setIsCallingApi(false);
        }
    };

    if (auth.isLoading) {
        return <div>Loading…</div>;
    }
    if (auth.error) {
        return <div>Error: {auth.error.message}</div>;
    }

    if (!auth.isAuthenticated) {
        return (
            <section id="center">
                <div className="hero">
                    <button onClick={() => auth.signinRedirect()}>Sign in</button>
                </div>
            </section>
        );
    }

    const signOutCognito = async () => {
        // Clear local app state first
        await auth.removeUser();

        const cognitoDomain = import.meta.env.VITE_OIDC_AUTHORITY; // Hosted UI domain
        const clientId = import.meta.env.VITE_OIDC_CLIENT_ID;
        const logoutUri = import.meta.env.VITE_OIDC_POST_LOGOUT_REDIRECT_URI;

        if (!cognitoDomain || !clientId || !logoutUri) {
            console.error("Missing logout env vars", {cognitoDomain, clientId, logoutUri});
            return;
        }

        window.location.href =
            `${cognitoDomain}/logout?client_id=${clientId}&logout_uri=${encodeURIComponent(logoutUri)}`;
    };

    return (
        <section id="center">
            <h1>Aplicatia lu Sorinu</h1>
            <pre style={{margin: 0}}>Hello: {String(auth.user?.profile?.email ?? "")}</pre>

            <div style={{display: "flex", gap: 8, marginTop: 12}}>
                <button onClick={signOutCognito}>Sign out</button>

                <button onClick={onCallGetUser} disabled={isCallingApi}>
                    {isCallingApi ? "Calling…" : "Call getUser"}
                </button>
            </div>

            {error && <pre style={{color: "crimson"}}>{error}</pre>}
            {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
        </section>
    );
}

export default App;