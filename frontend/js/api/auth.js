import { apiRequest }
from "./client.js";

export function login(
    username,
    password
) {
    return apiRequest(
        "POST",
        "/auth/login",
        {
            username,
            password
        }
    );
}

export function checkSession() {
    return apiRequest(
        "GET",
        "/auth/status"
    );
}