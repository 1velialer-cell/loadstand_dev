import { connectRunLogs } from "../api/run-logs.js";
import { LiveLogConsole } from "../components/live-log-console.js";
let currentSocket = null;
export async function showRunLive(runId) {
    const panel = document.getElementById("run-live-panel");
    const statusElement = document.getElementById("live-status");
    const progressElement = document.getElementById("live-progress");
    const logsElement = document.getElementById("live-logs");
    panel.classList.remove("hidden");
    const consoleView = new LiveLogConsole(logsElement);
    consoleView.clear();
    statusElement.textContent = "CONNECTING";
    progressElement.value = 0;
    if (currentSocket) {
        currentSocket.close();
    }
    currentSocket = connectRunLogs(runId,
        {
            onOpen() {statusElement.textContent = "CONNECTED";},
            onStatus(data) {statusElement.textContent = data.status;},
            onProgress(data) {progressElement.value = data.value;},
            onStdout(data) {consoleView.append(data.text);},
            onStderr(data) {consoleView.append(data.text);},
            onResult(data) {progressElement.value = 100; consoleView.append(`\n\nRun finished (${data.status})\n`);},
            onRunError(data) {consoleView.append(`\nERROR: ${data.message}\n`);},
            onClose() {statusElement.textContent = "DISCONNECTED";
            }
        }
    );
}