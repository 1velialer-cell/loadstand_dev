import { apiRequest } from "./client.js";

export function executeSSHCommand(nodeId, payload) {
    return apiRequest("POST", `/ssh/${nodeId}/execute`, payload);
}

export function resetSSHConnection(nodeId) {
    return apiRequest("POST", `/ssh/${nodeId}/reset`);
}

export function getSSHConnectionStatus(nodeId) {
    return apiRequest("GET", `/ssh/${nodeId}/status`);
}

export function getSSHCommand(commandId) {
    return apiRequest("GET", `/ssh/commands/${commandId}`);
}

export function stopSSHCommand(commandId) {
    return apiRequest("POST", `/ssh/commands/${commandId}/stop`);
}
