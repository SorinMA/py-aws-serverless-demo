export type GetUserResponse = {
    message: string;
    updatedAttributes?: unknown;
};

function getApiBaseUrl(): string {
    const url = import.meta.env.VITE_API_BASE_URL as string | undefined;
    if (!url) throw new Error("Missing VITE_API_BASE_URL");
    return url.replace(/\/+$/, ""); // remove trailing slashes
}

function getApiKey(): string {
    const apiKey = import.meta.env.VITE_API_KEY as string | undefined;
    if (!apiKey) throw new Error("Missing VITE_API_KEY");
    return apiKey;
}

export async function getUser(params: { email: string; accessToken: string; signal?: AbortSignal }) {
    const res = await fetch(
        `${getApiBaseUrl()}/get-user/${encodeURIComponent(params.email)}`,
        {
            method: "GET",
            signal: params.signal,
            headers: {
                Authorization: `Bearer ${params.accessToken}`,
                "x-api-key": getApiKey()
            },
        }
    );

    if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body?.error ?? `getUser failed: ${res.status} ${res.statusText}`);
    }
    return (await res.json()) as GetUserResponse;
}