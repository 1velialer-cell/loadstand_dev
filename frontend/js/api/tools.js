import { apiRequest }
from "./client.js";

export function getTools() {
    return apiRequest(
        "GET",
        "/tools"
    );
}

export function runToolApi(script) {
    return apiRequest(
        "POST",
        "/tools/run",
        {
            name: script
        }
    );
}