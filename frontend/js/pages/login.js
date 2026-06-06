import {
    login,
    checkSession
} from "../api/auth.js";
const authKey = "ls_token";
const el = id => document.getElementById(id);
const MESSAGES = {
    loginError: "Неверные учётные данные",
    networkError: "Ошибка сети"
};

export function showLogin() {
    el("login-card")
        .classList
        .remove("hidden");
    el("app-ui")
        .classList
        .add("hidden");
}

export function showMain() {
    el("login-card")
        .classList
        .add("hidden");
    el("app-ui")
        .classList
        .remove("hidden");
}

export function logout() {
    localStorage.removeItem(authKey);
    showLogin();
}

export async function tryRestore() {
    const token = localStorage.getItem(authKey);
    if (!token) {
        showLogin();
        return;
    }
    try {
        await checkSession();
        showMain();
    } catch {
        localStorage.removeItem(authKey);
        showLogin();
    }
}

export function initLoginPage() {
    el("btn-login")
        .addEventListener(
            "click",
            async () => {
                const u =
                    el("username")
                        .value
                        .trim();
                const p =
                    el("password")
                        .value
                        .trim();
                const errEl =
                    el("login-error");
                errEl.textContent = "";
                try {
                    const data = await login(u,p);
                    localStorage.setItem(authKey,data.token);
                    el(
                        "user-badge"
                    ).textContent =
                        u || "user";
                    showMain();
                } catch (err) {
                    if (
                        err.message
                            ?.startsWith(
                                "HTTP 401"
                            )
                    ) {
                        errEl.textContent =
                            MESSAGES.loginError;
                    } else {
                        errEl.textContent =
                            MESSAGES.networkError;
                    }
                }
            }
        );
    tryRestore();
}