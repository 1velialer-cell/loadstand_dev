const routes = {};
import { showServersPage } from "../pages/servers.js";
import { showToolPage } from "../pages/tools.js";
import { showRunsPage} from "../pages/runs.js";
export function registerRoute(path,handler) {routes[path] = handler;}
export function navigate(path) {history.pushState({},"",path);
    renderRoute();
}

export function renderRoute() {
    const path = window.location.pathname;
    const handler = routes[path];
    if (handler) {
        handler();
        return;
    }
    navigate("/smoke");
}

registerRoute("/smoke",() => showToolPage("smoke"));
registerRoute("/loading",() => showToolPage("loading"));
registerRoute("/stability",() => showToolPage("stability"));
registerRoute("/servers",showServersPage);
registerRoute("/runs", showRunsPage);

window.addEventListener("popstate",renderRoute);