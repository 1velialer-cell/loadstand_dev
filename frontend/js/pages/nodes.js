import {getNodes,createNode,updateNode,deleteNode,checkNode} from "../api/nodes.js";
import { hideAllPanels } from "../utils/panels.js";
const el = (id) => document.getElementById(id);
let editingNodeId = null;

function clearForm() {
    el("node-name").value = "";
    el("node-host").value = "";
    el("node-port").value = "";
    el("node-role").value = "MEDIA_SERVER";
    editingNodeId = null;
    el("node-save-btn").textContent = "Добавить";
}

function renderNodes(nodes) {
    const container = el("nodes-list");
    container.innerHTML = "";
    nodes.forEach(node => {
        const item = document.createElement("div");
        item.className = "node-card";
        item.innerHTML = `
            <div class="node-title">${node.name}</div>
            <div class="node-meta">${node.host}:${node.port}</div>
            <div class="node-meta">${node.role}</div>
            <div class="node-meta status ${node.status}">${node.status}</div>

            <div class="node-actions">
                <button class="btn small" data-edit="${node.id}">Edit</button>
                <button class="btn small danger" data-del="${node.id}">Delete</button>
                <button class="btn small" data-check="${node.id}">Check</button>
            </div>
        `;
        container.appendChild(item);
    });
    container.querySelectorAll("[data-edit]").forEach(b =>b.onclick = () => editNode(b.dataset.edit));
    container.querySelectorAll("[data-del]").forEach(b =>b.onclick = () => removeNode(b.dataset.del));
    container.querySelectorAll("[data-check]").forEach(b =>b.onclick = () => checkNodeAction(b.dataset.check));
}

export async function loadNodes() {
    const nodes = await getNodes();
    renderNodes(nodes);
}

async function saveNode() {
    const data = {
        name: el("node-name").value.trim(),
        host: el("node-host").value.trim(),
        port: Number(el("node-port").value),
        role: el("node-role").value
    };
    if (editingNodeId) {
        await updateNode(editingNodeId, data);
    } else {
        await createNode(data);
    }
    clearForm();
    await loadNodes();
}

export async function editNode(id) {
    const nodes = await getNodes();
    const node = nodes.find(n => n.id === id);
    editingNodeId = id;
    el("node-name").value = node.name;
    el("node-host").value = node.host;
    el("node-port").value = node.port;
    el("node-role").value = node.role;
    el("node-save-btn").textContent = "Сохранить";
}

export async function removeNode(id) {
    await deleteNode(id);
    await loadNodes();
}

export async function checkNodeAction(id) {
    await checkNode(id);
    await loadNodes();
}

export function initNodesPage() {
    const btn = el("node-save-btn");
    if (btn) btn.onclick = saveNode;
    window.editNode = editNode;
    window.removeNode = removeNode;
    loadNodes();
}

import { setActiveTab } from "../router/router.js";

export function showNodesPage() {
    hideAllPanels();
    document.getElementById("nodes-panel").classList.remove("hidden");
    setActiveTab("/nodes");
    loadNodes();
}
