export function connectRunLogs(runId, handlers = {}) {
    const protocol =window.location.protocol === "https:"
            ? "wss"
            : "ws";
    const ws = new WebSocket(`${protocol}://${window.location.host}/runs/${runId}/ws`);
    ws.onopen = () => {handlers.onOpen?.();};
    ws.onclose = () => {handlers.onClose?.();};
    ws.onerror = error => {handlers.onError?.(error);};
    ws.onmessage = event => {
        const data = JSON.parse(event.data);
        switch (data.type) {
            case "stdout":
                handlers.onStdout?.(data);
                break;
            case "stderr":
                handlers.onStderr?.(data);
                break;
            case "status":
                handlers.onStatus?.(data);
                break;
            case "progress":
                handlers.onProgress?.(data);
                break;
            case "result":
                handlers.onResult?.(data);
                break;
            case "error":
                handlers.onRunError?.(data);
                break;
        }
    };
    return ws;
}