import { apiRequest } from "./client.js";

export function createRun(payload) {
    return apiRequest("POST","/runs",payload);
}

export function getRuns() {
    return apiRequest("GET","/runs");
}

export function getRun(runId) {
    return apiRequest("GET",`/runs/${runId}`);
}

export function getRunResult(runId) {
    return apiRequest("GET",`/runs/${runId}/result`);
}