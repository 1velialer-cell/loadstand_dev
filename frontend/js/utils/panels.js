export function hideAllPanels() {
    document.querySelectorAll(".panel").forEach(panel => {
        panel.classList.add("hidden");
    });
}