import { navigate } from "../router/router.js";

export function initSidebar() {
    document.querySelectorAll(".tab").forEach(btn => {
        btn.onclick = () => {
            const route = btn.dataset.route;
            if (route) navigate(route);
        };
    });
}