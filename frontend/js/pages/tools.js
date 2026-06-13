import {createRun,getRunResult} from "../api/runs.js";
import { hideAllPanels } from "../utils/panels.js";
import { setActiveTab } from "../router/router.js";
const el = id => document.getElementById(id);
const MESSAGES = {
    testSuccess: "✅ Тест завершён",
    testFailed: "❌ Тест провален"
};
const tabToScript = {
    smoke:"smoke-test.py",
    loading:"load-test.py",
    stability:"stability-test.py"
};

function escapeHtml(text) {
    return String(text)
        .replace(/&/g,"&amp;")
        .replace(/</g,"&lt;")
        .replace(/>/g,"&gt;");
}

export async function runTool(tabName) {
    const script = tabToScript[tabName];
    const outputEl = el("tool-output");
    if (!outputEl) {
        return;
    }
    outputEl.innerHTML = `<span style="color:#888;">🚀 Запуск ${script}...</span><br><br>`;
    try {
        const run = await createRun({tool_name: script});
        const result = await getRunResult(run.id);
        let html =`<strong>${MESSAGES.testSuccess}</strong><br><br>`;
        if (result.status) {
            html +=`<strong>Статус:</strong> ${result.status}<br>`;
        }
        if (result.return_code !== undefined) {
            const color = result.return_code === 0
                    ? "#00ff00"
                    : "#ff4444";
            html += `<strong>Код возврата:</strong> <span style="color:${color}">${result.return_code}</span><br><br>`;
        }
        if (result.stdout?.trim()) {
            html +=`<strong>Вывод:</strong><br><pre>${escapeHtml(result.stdout)}</pre>`;
        }
        if (result.stderr?.trim()) {
            html +=`<strong>Ошибки:</strong><br><pre>${escapeHtml(result.stderr)}</pre>`;
        }
        outputEl.innerHTML = html;
    } catch (err) {
        outputEl.innerHTML =`<span style="color:red;">${err.message}</span>`;
    }
}

export function initToolsPage() {
    ["smoke","loading","stability"].forEach(name => {
        const btn = el(`${name}_button`);
        if (!btn) {return;}
        btn.addEventListener("click",() => runTool(name));
    });
}

export function showToolPage(toolName) {
    hideAllPanels();
    const outputEl = el("tool-output");
    if (outputEl) {outputEl.innerHTML = "";}
    el("runs-panel").classList.add("hidden");
    el("tests-panel").classList.remove("hidden");
    el("panel-title").textContent = toolName;
    el("smoke_button").classList.toggle("hidden",toolName !== "smoke");
    el("loading_button").classList.toggle("hidden",toolName !== "loading");
    el("stability_button").classList.toggle("hidden",toolName !== "stability");
    setActiveTab(`/${toolName}`);
}

