import { apiRequest } from "./client.js";

export const createNode = (data) =>
    apiRequest("POST", "/nodes", data);

export const getNodes = () =>
    apiRequest("GET", "/nodes");

export const updateNode = (id, data) =>
    apiRequest("PATCH", `/nodes/${id}`, data);

export const deleteNode = (id) =>
    apiRequest("DELETE", `/nodes/${id}`);

export const checkNode = (id) =>
    apiRequest("POST", `/nodes/${id}/check`);