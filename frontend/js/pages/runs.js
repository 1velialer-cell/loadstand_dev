const el = id => document.getElementById(id);

export function showRunsPage() {
    el("tests-panel")
        .classList.add("hidden");
    el("servers-panel")
        .classList.add("hidden");
    el("runs-panel")
        .classList.remove("hidden");
}