import {getMediaServers,getLoadServers,getServer,createServer,updateServer,removeServer} from "../api/servers.js";
const el = id =>document.getElementById(id);
let editingServerId = null;

function clearServerForm() {
    el("srv-name").value = "";
    el("srv-host").value = "";
    el("srv-login").value = "";
    el("srv-password").value = "";
    el("srv-type").value = "";
    editingServerId = null;
    el("add-server-btn").textContent = "Добавить";
}

function renderServerList(containerId,servers) {
    const container = el(containerId);
    container.innerHTML = "";
    servers.forEach(
        server => {
            const item = document.createElement("div");
            item.className = "server-item";
            item.textContent = server.name;
            item.onclick = () => showServer(server.id);
            container.appendChild(item);
        }
    );
}

export async function loadServers() {
    const media = await getMediaServers();
    const load = await getLoadServers();
    renderServerList("media-list",media);
    renderServerList("load-list",load);
}

export async function showServer(id) {
    const server =await getServer(id);
    const panel = el("server-details");
    panel.classList.remove("hidden");
    panel.innerHTML = `
        <h3>${server.name}</h3>
        <p>Host: ${server.host}</p>
        <p>Login: ${server.ssh_login}</p>
        <p>Type: ${server.type}</p>
        <button onclick="editServer('${server.id}')">
            Редактировать
        </button>
        <button onclick="deleteServer('${server.id}')">
            Удалить
        </button>`;}

async function saveServer() {
    const data = {
        name: el("srv-name").value.trim(),
        host: el("srv-host").value.trim(),
        ssh_login: el("srv-login").value.trim(),
        ssh_password:el("srv-password").value.trim(),
        type: el("srv-type").value};
    if (editingServerId) {
        await updateServer({id:editingServerId,...data});}
    else {
        await createServer(data);}
    clearServerForm();
    await loadServers();
}

export async function editServer(id) {
    const server = await getServer(id);
    editingServerId = id;
    el("srv-name").value = server.name;
    el("srv-host").value = server.host;
    el("srv-login").value = server.ssh_login;
    el("srv-password").value = server.ssh_password;
    el("srv-type").value = server.type;
}

export async function deleteServer(id) {
    await removeServer(id);
    await loadServers();
}

export function initServersPage() {
    const btn =el("add-server-btn");
    if (btn) {btn.addEventListener("click",saveServer);}
    window.editServer = editServer;
    window.deleteServer = deleteServer;
}

export async function showServersPage() {
    el("tests-panel").classList.add("hidden");
    el("runs-panel").classList.add("hidden");
    el("servers-panel").classList.remove("hidden");
    await loadServers();
}
