import { apiRequest }
from "./client.js";

export function getMediaServers() {
    return apiRequest(
        "GET",
        "/server/media"
    );
}

export function getLoadServers() {
    return apiRequest(
        "GET",
        "/server/load"
    );
}

export function getServer(id) {
    return apiRequest(
        "GET",
        `/server?id=${id}`
    );
}

export function createServer(data) {
    return apiRequest(
        "POST",
        "/server",
        data
    );
}

export function updateServer(data) {
    return apiRequest(
        "PATCH",
        "/server",
        data
    );
}

export function removeServer(id) {
    return apiRequest(
        "DELETE",
        "/server",
        { id }
    );
}