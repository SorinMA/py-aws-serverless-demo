import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import { useAuth } from "react-oidc-context";
import './App.css'

function App() {
  const auth = useAuth();

  const signOutRedirect = () => {
    const clientId = "7omb93dm674444e9s5mlkcrjai";
    const logoutUri = "https://d2hrj96483he4t.cloudfront.net/";
    const cognitoDomain = "https://backend-dev-544474104881-cupd.auth.eu-north-1.amazoncognito.com";
    window.location.href = `${cognitoDomain}/logout?client_id=${clientId}&logout_uri=${encodeURIComponent(logoutUri)}`;
  };

  if (auth.isLoading) {
    return <div>Loading...</div>;
  }

  if (auth.error) {
    return <div>Encountering error... {auth.error.message}</div>;
  }

  if (auth.isAuthenticated) {
    return (
      <>
        <section id="center">
          <div className="hero">
            <img src={heroImg} className="base" width="170" height="179" alt="" />
            <img src={reactLogo} className="framework" alt="React logo" />
            <img src={viteLogo} className="vite" alt="Vite logo" />
          </div>
          <div>
            <h1>Aplicatia lu Sorinu</h1>
          </div>
        </section>
        <section id="next-steps" style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <pre style={{ margin: 0 }}>Hello: {auth.user?.profile.email}</pre>
          <pre style={{ margin: 0 }}>ID Token: {auth.user?.id_token}</pre>
          <pre style={{ margin: 0 }}>Access Token: {auth.user?.access_token}</pre>
          <pre style={{ margin: 0 }}>Refresh Token: {auth.user?.refresh_token}</pre>
          <button onClick={() => auth.removeUser()}>Sign out</button>
        </section>
        <div className="ticks"></div>
        <section id="spacer"></section>
      </>
    )
  }

  return (
    <section id="center">
      <div className="hero">
        <button onClick={() => auth.signinRedirect()}>Sign in</button>
        <button onClick={() => signOutRedirect()}>Sign out</button>
      </div>
    </section>
  );
}

export default App
