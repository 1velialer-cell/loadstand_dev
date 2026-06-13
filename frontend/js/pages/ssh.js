import { executeSSHCommand, getSSHCommand, stopSSHCommand } from "../api/ssh.js";
import { getNodes } from "../api/nodes.js";
import { hideAllPanels } from "../utils/panels.js";
import { setActiveTab } from "../router/router.js";
const el = id => document.getElementById(id);
let currentCommandId = null;
let currentNodeId = null;

async function populateNodeOptions() {
    const nodeSelect = el("ssh-node");
    nodeSelect.innerHTML = "<option value=\"\">Select node</option>";
    try {
        const nodes = await getNodes();
        nodes.forEach(node => {
            const option = document.createElement("option");
            option.value = node.id;
            option.textContent = `${node.name} (${node.host}:${node.port})`;
            nodeSelect.appendChild(option);
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
    el("ssh-output").textContent = "";
    el("ssh-status").textContent = "";
}

export function initSSHPage() {
    const runBtn = el("ssh-run-btn");
    const stopBtn = el("ssh-stop-btn");
    if (runBtn) {
        runBtn.addEventListener("click", runSSHCommand);
    }
    if (stopBtn) {
        stopBtn.addEventListener("click", stopSSHCommandAction);
    }
}

async function runSSHCommand() {
    const nodeId = el("ssh-node").value;
    const command = el("ssh-command").value.trim();
    if (!nodeId || !command) {
        el("ssh-status").textContent = "Node and command required.";
        return;
    }
    el("ssh-status").textContent = "Executing...";
    try {
        const result = await executeSSHCommand(nodeId, { command });
        currentCommandId = result.command_id;
        currentNodeId = nodeId;
        el("ssh-status").textContent = `Running: ${currentCommandId}`;
        pollSSHResult();
    } catch (err) {
        el("ssh-status").textContent = err.message || "SSH execution failed.";
    }
}

async function pollSSHResult() {
    if (!currentCommandId) {
        return;
    }
    try {
        const status = await getSSHCommand(currentCommandId);
        el("ssh-output").textContent = `stdout:\n${status.stdout || ""}\nstderr:\n${status.stderr || ""}`;
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
        el("ssh-status").textContent = "No running command.";
        return;
    }
    try {
        const result = await stopSSHCommand(currentCommandId);
        el("ssh-status").textContent = `Stopped: ${result.status}`;
        el("ssh-output").textContent = `stdout:\n${result.stdout || ""}\nstderr:\n${result.stderr || ""}`;
    } catch (err) {
        el("ssh-status").textContent = err.message || "Failed to stop command.";
    }
}
