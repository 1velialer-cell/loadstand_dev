import { executeSSHCommand, getSSHCommand, stopSSHCommand, resetSSHConnection, getSSHConnectionStatus } from "../api/ssh.js";
import { getNodes } from "../api/nodes.js";
import { hideAllPanels } from "../utils/panels.js";
import { setActiveTab } from "../router/router.js";
const el = id => document.getElementById(id);
let currentCommandId = null;
let currentNodeId = null;

function setSSHStatus(message, statusClass = null) {
    const statusEl = el("ssh-status");
    if (!statusEl) return;
    statusEl.textContent = message;
    statusEl.classList.remove("online", "offline", "unknown");
    if (statusClass) {
        statusEl.classList.add(statusClass);
    }
}

async function populateNodeOptions() {
    const nodeSelect = el("ssh-node");
    try {
        const nodes = await getNodes();
        // Очищаем и создаём Set для гарантирования уникальности
        const nodeIds = new Set();
        nodeSelect.innerHTML = "<option value=\"\">Select node</option>";
        nodes.forEach(node => {
            if (!nodeIds.has(node.id)) {
                nodeIds.add(node.id);
                const option = document.createElement("option");
                option.value = node.id;
                option.textContent = `${node.name} (${node.host}:${node.port})`;
                nodeSelect.appendChild(option);
            }
        });
    } catch (err) {
        el("ssh-status").textContent = "Failed to load nodes.";
    }
}

export async function showSSHPage() {
    hideAllPanels();
    el("ssh-panel").classList.remove("hidden");
    setActiveTab("/ssh");
    currentCommandId = null;
    currentNodeId = null;
    await populateNodeOptions();
    el("ssh-command").value = "";
    el("ssh-stdout").textContent = "";
    el("ssh-stderr").textContent = "";
    setSSHStatus("Select a node to check SSH status.", "unknown");
    await refreshSSHStatus();
}

export function initSSHPage() {
    const runBtn = el("ssh-run-btn");
    const stopBtn = el("ssh-stop-btn");
    const resetBtn = el("ssh-reset-btn");
    if (runBtn) {
        runBtn.addEventListener("click", runSSHCommand);
    }
    if (stopBtn) {
        stopBtn.addEventListener("click", stopSSHCommandAction);
    }
    if (resetBtn) {
        resetBtn.addEventListener("click", resetSSHConnectionAction);
    }
    const nodeSelect = el("ssh-node");
    if (nodeSelect) {
        nodeSelect.addEventListener("change", refreshSSHStatus);
    }
    document.addEventListener("visibilitychange", () => {
        if (document.visibilityState === "visible" && window.location.pathname === "/ssh") {
            refreshSSHStatus();
        }
    });
    window.addEventListener("pageshow", (event) => {
        if (window.location.pathname === "/ssh") {
            refreshSSHStatus();
        }
    });
}

async function runSSHCommand() {
    const nodeId = el("ssh-node").value;
    const command = el("ssh-command").value.trim();
    if (!nodeId || !command) {
        setSSHStatus("Node and command required.", "unknown");
        return;
    }
    setSSHStatus("Executing...", "unknown");
    try {
        const result = await executeSSHCommand(nodeId, { command });
        currentCommandId = result.command_id;
        currentNodeId = nodeId;
        setSSHStatus(`Running: ${currentCommandId}`, "unknown");
        pollSSHResult();
    } catch (err) {
        setSSHStatus(err.message || "SSH execution failed.", "offline");
    }
}

async function refreshSSHStatus() {
    const nodeId = el("ssh-node")?.value;
    if (!nodeId) {
        setSSHStatus("Select a node to check SSH status.", "unknown");
        return;
    }
    setSSHStatus("Refreshing SSH status...", "unknown");
    try {
        const result = await getSSHConnectionStatus(nodeId);
        const status = result.status?.toLowerCase() || "unknown";
        setSSHStatus(`SSH status: ${result.status}`, status);
    } catch (err) {
        setSSHStatus(err.message || "SSH status unavailable.", "offline");
    }
}

async function resetSSHConnectionAction() {
    const nodeId = el("ssh-node")?.value;
    if (!nodeId) {
        setSSHStatus("Select a node to reset.", "unknown");
        return;
    }
    setSSHStatus("Resetting SSH connection...", "unknown");
    try {
        await resetSSHConnection(nodeId);
        setSSHStatus("SSH connection reset.", "unknown");
        await refreshSSHStatus();
    } catch (err) {
        setSSHStatus(err.message || "SSH reset failed.", "offline");
    }
}

async function pollSSHResult() {
    if (!currentCommandId) {
        return;
    }
    try {
        const status = await getSSHCommand(currentCommandId);
        el("ssh-stdout").textContent = status.stdout || "";
        el("ssh-stderr").textContent = status.stderr || "";
        if (status.status === "running") {
            setTimeout(pollSSHResult, 1000);
        } else {
            el("ssh-status").textContent = `Completed: ${status.return_code}`;
        }
    } catch (err) {
        el("ssh-status").textContent = err.message || "Failed to fetch SSH status.";
    }
}

async function stopSSHCommandAction() {
    if (!currentCommandId) {
        setSSHStatus("No running command.", "unknown");
        return;
    }
    try {
        const result = await stopSSHCommand(currentCommandId);
        setSSHStatus(`Stopped: ${result.status}`, "unknown");
        el("ssh-stdout").textContent = result.stdout || "";
        el("ssh-stderr").textContent = result.stderr || "";
    } catch (err) {
        setSSHStatus(err.message || "Failed to stop command.", "offline");
    }
}
