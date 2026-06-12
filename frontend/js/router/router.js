import { showServersPage } from "../pages/servers.js";
import { showToolPage } from "../pages/tools.js";
import { showRunsPage } from "../pages/runs.js";
import { showNodesPage } from "../pages/nodes.js";

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
    document.getElementById("servers-panel")
        ?.classList.add("hidden");
    document.getElementById("runs-panel")
        ?.classList.add("hidden");
    document.getElementById("nodes-panel")
        ?.classList.add("hidden");
}

export function renderRoute() {
    const path = window.location.pathname;
    const handler = routes[path];
    if (handler) {
        hideAllPages();
        handler();
        return;
    }
    navigate("/smoke");
}

registerRoute("/smoke", () => showToolPage("smoke"));
registerRoute("/loading", () => showToolPage("loading"));
registerRoute("/stability", () => showToolPage("stability"));
registerRoute("/servers", showServersPage);
registerRoute("/runs", showRunsPage);
registerRoute("/nodes", showNodesPage);

window.addEventListener("popstate", renderRoute);