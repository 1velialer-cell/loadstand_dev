import { getRuns,getRunResult } from "../api/runs.js";
import { authState } from "../state/auth.js";
import { hideAllPanels } from "../utils/panels.js";
const el = id => document.getElementById(id);

import { setActiveTab } from "../router/router.js";

export async function showRunsPage() {
    hideAllPanels();
    el("runs-panel").classList.remove("hidden");
    setActiveTab("/runs");
    await loadRuns();
}

function formatDate(value) {
    if (!value) {return "-";}
    return new Date(value).toLocaleString("ru-RU");
}
function formatDuration(startedAt, finishedAt) {
    if (!startedAt || !finishedAt) {return "-";}
    const start = new Date(startedAt);
    const finish = new Date(finishedAt);
    return ((finish - start) / 1000).toFixed(2) + " sec";
}

async function loadRuns() {
    const runs = await getRuns(authState.token);
    console.log(runs);
    renderRuns(runs);
}

function bindResultButtons() {
    document.querySelectorAll(".show-result-btn").forEach(btn => {
        btn.addEventListener("click",
            async () => {
                const runId = btn.dataset.runId;
                const result = await getRunResult(runId);
                showResultModal(result);
            }
        );
    });
}

function showResultModal(result) {
    alert(
        result.stdout ||
        result.stderr ||
        "Нет данных");
}

function renderRuns(runs) {
    const tbody = document.getElementById("runs-body");
    if (!tbody) {
        return;
    }
    tbody.innerHTML = "";
    for (const run of runs) {
        const duration = formatDuration(run.started_at,run.finished_at);
        const statusClass =
            run.status === "FINISHED"
                ? "status-finished"
                : run.status === "FAILED"
                    ? "status-failed"
                    : "status-created";
        tbody.insertAdjacentHTML("beforeend",
            `
            <tr>
                <td class="run-tool">
                    ${run.id}
                </td>
                <td>
                    ${run.tool_name}
                </td>
                <td>
                    <span class="${statusClass}">
                        ${run.status}
                    </span>
                </td>
                <td>
                    ${formatDate(run.started_at)}
                </td>
                <td>
                    ${formatDate(run.finished_at)}
                </td>
                <td>
                    ${duration}
                </td>
            </tr>
            `
        );
    }
    bindResultButtons();
}