import { navigate } from "../router/router.js";

export function initNavbar() {
    document.querySelectorAll("[data-route]").forEach(btn => {
        btn.addEventListener("click", () => {
            navigate(btn.dataset.route);
        });
    });
}