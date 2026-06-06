const API_BASE = "";
const AUTH_KEY = "ls_token";

export async function apiRequest(
    method,
    url,
    body = null
) {
    const token = localStorage.getItem(AUTH_KEY);
    const headers = {"Content-Type":"application/json"};
    if (token) {
        headers.Authorization =
        `Bearer ${token}`;
    }

    const response =await fetch(`${API_BASE}${url}`,{
                method,
                headers,
                body: body
                    ? JSON.stringify(body)
                    : null
            }
        );

    if (response.status === 401) {
        throw {
            unauthorized: true
        };
    }

    if (!response.ok) {
        const text =
            await response.text();
        throw new Error(
            `HTTP ${response.status}: ${text}`
        );
    }

    if (response.status === 204) {
        return null;
    }

    return response.json();
}