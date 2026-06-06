import {initLoginPage} from "./pages/login.js";
import {initToolsPage} from "./pages/tools.js";
import {initServersPage} from "./pages/servers.js";
import {showRunsPage} from "./pages/runs.js";
import {navigate,renderRoute} from "./router/router.js";

function initTabs() {
    document.querySelectorAll(".tab").forEach(tab => {
      tab.addEventListener("click",() => navigate(tab.dataset.route));
    });
}

function bootstrap() {
    initLoginPage();
    initToolsPage();
    initServersPage();
    initTabs();
    renderRoute();
}
bootstrap();