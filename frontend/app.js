const API = window.location.origin;
const authKey = "ls_token";
const el = id => document.getElementById(id);

let currentTab = "smoke";

async function apiFetch(path, method = "GET", body) {
  const token = localStorage.getItem(authKey);
  const headers = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = "Bearer " + token;

  const res = await fetch(API + path, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined
  });

  if (res.status === 401) throw { unauthorized: true };
  if (res.status === 204) return null;

  const txt = await res.text();
  try { return JSON.parse(txt); } catch { return txt; }
}

// ====================== Запуск тестов ======================
const tabToScript = {
  smoke: "smoke-test.py",
  loading: "load-test.py",
  stability: "stability-test.py"
};

async function runTool(tabName) {
  const script = tabToScript[tabName];
  const outputEl = el("tool-output");

  if (!outputEl) return;

  outputEl.innerHTML = `<span style="color:#888;">🚀 Запуск ${script}...</span><br><br>`;
  outputEl.scrollTop = outputEl.scrollHeight;

  try {
    const result = await apiFetch("/api/run-tool", "POST", { name: script });

    let html = `<strong>✅ Тест завершён</strong><br><br>`;

    if (result.status) {
      html += `<strong>Статус:</strong> ${result.status}<br>`;
    }
    if (result.returncode !== undefined) {
      const color = result.returncode === 0 ? "#00ff00" : "#ff4444";
      html += `<strong>Код возврата:</strong> <span style="color:${color}">${result.returncode}</span><br><br>`;
    }

    if (result.stdout?.trim()) {
      html += `<strong>Вывод:</strong><br><pre style="background:#1e1e1e; color:#ddd; padding:12px; border-radius:6px; white-space:pre-wrap; font-size:14px;">${escapeHtml(result.stdout)}</pre><br>`;
    }

    if (result.stderr?.trim()) {
      html += `<strong>Ошибки:</strong><br><pre style="background:#330000; color:#ff8888; padding:12px; border-radius:6px; white-space:pre-wrap; font-size:14px;">${escapeHtml(result.stderr)}</pre><br>`;
    }

    outputEl.innerHTML = html;
    outputEl.scrollTop = outputEl.scrollHeight;

  } catch (e) {
    if (e && e.unauthorized) {
      logout();
    } else {
      outputEl.innerHTML = `<span style="color:red;">❌ Ошибка запуска теста:<br>${escapeHtml(String(e))}</span>`;
    }
  }
}

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

// ====================== Табы ======================
document.querySelectorAll(".tab").forEach(tab => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    tab.classList.add("active");

    currentTab = tab.dataset.tab;
    el("panel-title").textContent = currentTab;

    el("smoke_button").classList.toggle("hidden", currentTab !== "smoke");
    el("loading_button").classList.toggle("hidden", currentTab !== "loading");
    el("stability_button").classList.toggle("hidden", currentTab !== "stability");

    if (el("tool-output")) el("tool-output").innerHTML = "";
  });
});

// Привязка кнопок Запуск
["smoke", "loading", "stability"].forEach(name => {
  const btn = el(`${name}_button`);
  if (btn) btn.addEventListener("click", () => runTool(name));
});

// ====================== Авторизация ======================
el("btn-login").addEventListener("click", async () => {
  const u = el("username").value.trim();
  const p = el("password").value.trim();
  const errEl = el("login-error");
  errEl.textContent = "";

  try {
    const r = await fetch(API + "/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: u, password: p })
    });

    if (!r.ok) {
      errEl.textContent = "Неверные учётные данные";
      return;
    }

    const data = await r.json();
    localStorage.setItem(authKey, data.token);
    el("user-badge").textContent = u || "user";
    showMain();
  } catch (err) {
    errEl.textContent = "Ошибка сети";
  }
});

function showLogin() {
  el("login-card").classList.remove("hidden");
  el("app-ui").classList.add("hidden");
}

function showMain() {
  el("login-card").classList.add("hidden");
  el("app-ui").classList.remove("hidden");
}

function logout() {
  localStorage.removeItem(authKey);
  showLogin();
}

async function tryRestore() {
  const token = localStorage.getItem(authKey);
  if (!token) { showLogin(); return; }

  try {
    await apiFetch("/api/status");
    showMain();
  } catch (e) {
    localStorage.removeItem(authKey);
    showLogin();
  }
}

// Инициализация
tryRestore();