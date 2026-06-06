import { apiRequest } from "./client.js";

export async function getRuns(token) {
    return apiRequest(
        "GET",
        "/runs",
        null,
        token
    );
}

export async function getRun(
    token,
    runId
) {
    return apiRequest(
        "GET",
        `/runs/${runId}`,
        null,
        token
    );
}

export async function createRun(
    token,
    payload
) {
    return apiRequest(
        "POST",
        "/runs",
        payload,
        token
    );
}