import {initLoginPage} from "./pages/login.js";
import {initToolsPage} from "./pages/tools.js";
import {initServersPage,loadServers} from "./pages/servers.js";
const el = id => document.getElementById(id);
let currentTab = "smoke";

function initTabs() {
  document.querySelectorAll(".tab")
  .forEach(tab => {
    tab.addEventListener("click",async () => {
      document.querySelectorAll(".tab")
      .forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      currentTab = tab.dataset.tab;
      const testPanel =document.querySelector(".panel.panel-wide");
      const serversPanel = el("servers-panel");
      if (currentTab ==="servers") {
        testPanel.classList.add("hidden");
        serversPanel.classList.remove("hidden");
        await loadServers();
        return;}
      serversPanel.classList.add("hidden");
      testPanel.classList.remove("hidden");
      el("panel-title").textContent =currentTab;
      el("smoke_button").classList.toggle("hidden",currentTab !=="smoke");
      el("tool-output").innerHTML ="";
      el("loading_button").classList.toggle("hidden",currentTab !=="loading");
      el("stability_button").classList.toggle("hidden",currentTab !=="stability");
      });
  });
}

function bootstrap() {
    initLoginPage();
    initToolsPage();
    initServersPage();
    initTabs();
}
bootstrap();