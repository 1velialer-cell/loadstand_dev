import { showToolPage } from "../pages/tools.js";
import { showRunsPage } from "../pages/runs.js";
import { showNodesPage } from "../pages/nodes.js";
import { showSSHPage } from "../pages/ssh.js";

const routes = {};

export function registerRoute(path, handler) {
    routes[path] = handler;
}

export function navigate(path) {
    history.pushState({}, "", path);
    renderRoute();
}

function hideAllPages() {
    document.getElementById("tests-panel")
        ?.classList.add("hidden");
    document.getElementById("runs-panel")
        ?.classList.add("hidden");
    document.getElementById("nodes-panel")
        ?.classList.add("hidden");
    document.getElementById("ssh-panel")
        ?.classList.add("hidden");
}

export function setActiveTab(path) {
    document.querySelectorAll(".tab").forEach(tab => {
        tab.classList.toggle("active", tab.dataset.route === path);
    });
}

export function renderRoute() {
    const path = window.location.pathname;
    const handler = routes[path];
    if (handler) {
        window.stopNodesAutoRefresh?.();
        hideAllPages();
        handler();
        return;
    }
    navigate("/smoke");
}

registerRoute("/smoke", () => showToolPage("smoke"));
registerRoute("/loading", () => showToolPage("loading"));
registerRoute("/stability", () => showToolPage("stability"));
registerRoute("/runs", showRunsPage);
registerRoute("/nodes", showNodesPage);
registerRoute("/ssh", showSSHPage);

window.addEventListener("popstate", renderRoute);