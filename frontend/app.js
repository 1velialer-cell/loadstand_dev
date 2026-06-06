const API = window.location.origin;
const authKey = "ls_token";
const el = id => document.getElementById(id);
const testPanel = el("tests-panel");

const MESSAGES = {
  loginError: "Неверные учётные данные",
  networkError: "Ошибка сети",
  testStart: "🚀 Запуск",
  testSuccess: "✅ Тест завершён",
  unauthorized: "Сессия истекла"
};

let currentTab = "smoke";

const tabToScript = {
  smoke: "smoke-test.py",
  loading: "load-test.py",
  stability: "stability-test.py"
};

// ====================== API Helper ======================
async function apiFetch(endpoint, method = "GET", body = null) {
  const token = localStorage.getItem(authKey);
  const headers = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const options = { method, headers };
  if (body) options.body = JSON.stringify(body);

  const response = await fetch(API + endpoint, options);

  if (response.status === 401) {
    throw { unauthorized: true };
  }
  if (!response.ok) {
    const errorText = await response.text().catch(() => "");
    throw new Error(`HTTP ${response.status}: ${errorText}`);
  }
  return response.json();
}

// ====================== Запуск теста ======================
async function runTool(tabName) {
  const script = tabToScript[tabName];
  const outputEl = el("tool-output");

  if (!outputEl) return;

  outputEl.innerHTML = `<span style="color:#888;">🚀 Запуск ${script}...</span><br><br>`;
  outputEl.scrollTop = outputEl.scrollHeight;

  try {
    const result = await apiFetch("/tools/run", "POST", { name: script });

    let html = `<strong>${MESSAGES.testSuccess}</strong><br><br>`;

    if (result.status) html += `<strong>Статус:</strong> ${result.status}<br>`;
    if (result.returncode !== undefined) {
      const color = result.returncode === 0 ? "#00ff00" : "#ff4444";
      html += `<strong>Код возврата:</strong> <span style="color:${color}">${result.returncode}</span><br><br>`;
    }

    if (result.stdout?.trim()) {
      html += `<strong>Вывод:</strong><br><pre style="background:#1e1e1e;color:#ddd;padding:12px;border-radius:6px;white-space:pre-wrap;font-size:14px;">${escapeHtml(result.stdout)}</pre><br>`;
    }
    if (result.stderr?.trim()) {
      html += `<strong>Ошибки:</strong><br><pre style="background:#330000;color:#ff8888;padding:12px;border-radius:6px;white-space:pre-wrap;font-size:14px;">${escapeHtml(result.stderr)}</pre><br>`;
    }

    outputEl.innerHTML = html;
    outputEl.scrollTop = outputEl.scrollHeight;

  } catch (e) {
    if (e && e.unauthorized) {
      logout();
    } else {
      console.error(e);
      outputEl.innerHTML = `<span style="color:red;">❌ Ошибка: ${escapeHtml(e.message || String(e))}</span>`;
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
  tab.addEventListener("click", async () => {
    document
      .querySelectorAll(".tab")
      .forEach(t => t.classList.remove("active"));
    tab.classList.add("active");
    currentTab = tab.dataset.tab;
    const testPanel =
      document.querySelector(".panel.panel-wide");
    const serversPanel =
      el("servers-panel");
    if (currentTab === "servers") {

      testPanel.classList.add("hidden");
      serversPanel.classList.remove("hidden");
      await loadServers();
      return;
    }
    serversPanel.classList.add("hidden");
    testPanel.classList.remove("hidden");

    el("panel-title").textContent = currentTab;
    el("smoke_button")
      .classList.toggle(
        "hidden",
        currentTab !== "smoke"
      );
    el("loading_button")
      .classList.toggle(
        "hidden",
        currentTab !== "loading"
      );
    el("stability_button")
      .classList.toggle(
        "hidden",
        currentTab !== "stability"
      );
    el("tool-output").innerHTML = "";
  });
});

// Привязка кнопок
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
      errEl.textContent = MESSAGES.loginError;
      return;
    }

    const data = await r.json();
    localStorage.setItem(authKey, data.token);
    el("user-badge").textContent = u || "user";
    showMain();
  } catch (err) {
    errEl.textContent = MESSAGES.networkError;
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
    await apiFetch("/tools/run", "POST", { name: "smoke-test.py" }); // можно сделать отдельный /status позже
    showMain();
  } catch (e) {
    localStorage.removeItem(authKey);
    showLogin();
  }
}

//сервера.добавить
async function createServer() {
    const name = el("srv-name").value.trim();
    const host = el("srv-host").value.trim();
    const login = el("srv-login").value.trim();
    const password = el("srv-password").value.trim();
    const type = el("srv-type").value;
    if (
        !name ||
        !host ||
        !login ||
        !password ||
        !type
    ) {
        alert("Заполните все поля");
        return;
    }
    await apiFetch(
        "/server",
        "POST",
        {
            name,
            host,
            ssh_login: login,
            ssh_password: password,
            type
        }
    );
    clearServerForm();
    loadServers();
}
const addServerBtn =
  el("add-server-btn");
if (addServerBtn) {
  addServerBtn.addEventListener(
    "click",
    createServer
  );
}
//сервера.очистка формы
function clearServerForm() {
    el("srv-name").value = "";
    el("srv-host").value = "";
    el("srv-login").value = "";
    el("srv-password").value = "";
    el("srv-type").value = "";
}
//сервера.загрузить список
async function loadServers() {
    const media =
        await apiFetch("/server/media");
    const load =
        await apiFetch("/server/load");
    renderServerList(
        "media-list",
        media
    );
    renderServerList(
        "load-list",
        load
    );
}
//сервера.рендер
function renderServerList(
    containerId,
    servers) {
    const container = el(containerId);
    container.innerHTML = "";
    servers.forEach(server => {
        const item =
            document.createElement("div");
        item.className = "server-item";
        item.textContent =
            server.name;
        item.onclick =
            () => showServer(server.id);
        container.appendChild(item);
    });}
//сервера.показать
async function showServer(id) {
    const server =
        await apiFetch(
            `/server?id=${id}`);
    const panel =
        document.getElementById(
            "server-details");
    panel.classList.remove(
        "hidden");
    panel.innerHTML = `
        <h3>${server.name}</h3>
        <p>
            Host: ${server.host}
        </p>
        <p>
            Login: ${server.ssh_login}
        </p>
        <p>
            Type: ${server.type}
        </p>
        <button
            onclick="editServer('${server.id}')" disabled
        >
            Редактировать
        </button>
        <button
            onclick="deleteServer('${server.id}')"
        >
            Удалить
        </button>
    `;
}
//сервера.удалить
async function deleteServer(id) {
    await apiFetch(
      "/server",
      "DELETE",
      { id }
    );
    document
        .getElementById(
            "server-details"
        )
        .classList
        .add("hidden");
    loadServers();
}





// Инициализация
tryRestore();