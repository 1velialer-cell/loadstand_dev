import {initLoginPage} from "./pages/login.js";
import {initToolsPage} from "./pages/tools.js";
import {showRunsPage} from "./pages/runs.js";
import {initNodesPage} from "./pages/nodes.js";
import {initServersPage} from "./pages/servers.js";
import {navigate,renderRoute} from "./router/router.js";
import {initSidebar} from "./components/sidebar.js";
import {initNavbar} from "./components/navbar.js";

// document.addEventListener("DOMContentLoaded", () => {
//     initSidebar();
//     initServersPage();
//     initNodesPage();
//     renderRoute();
// });

function initTabs() {
    document.querySelectorAll(".tab").forEach(tab => {
      tab.addEventListener("click",() => navigate(tab.dataset.route));
    });
}

function bootstrap() {
    initNavbar();
    initLoginPage();
    initToolsPage();
    initServersPage();
    initTabs();
    renderRoute();
    initNodesPage();
}
bootstrap();
