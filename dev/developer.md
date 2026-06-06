## Общая информация
**Loadstand** — веб-система автоматизации запуска smoke, load и stability тестов.
**Цель:** Упростить и стандартизировать процесс запуска тестовых скриптов через удобный веб-интерфейс с возможностью дальнейшего масштабирования на несколько серверов.

## Текущий технологический стек
- **Backend**:
   FastAPI
   Uvicorn
   Pydantic
   AsyncIO
   Модульная структура (routers, services, models, core)
**Frontend**
   Vanilla JavaScript (ES Modules)
   HTML
   CSS
   SPA Router (History API)
**Выполнение тестов**: `asyncio.create_subprocess_exec`
**Авторизация**: token-based (in-memory)
**Язык**: Python 3.10+
**Отладка**: Прямой запуск на сервере

## Текущая архитектура
loadstand/
├── main.py
├── backend/
├────── core/
│      ├── config.py
│      └── sec.py
├────── models/
│      └── schemas.py
├────── routers/
│      ├── auth.py
│      ├── tools.py
│      ├── logo.py
│      └── servers.py
├────── services/
│      └── tool_executor.py
├────── storage.py
├── frontend/
├────── index.html
├────── styles.css
├────── js/
│       ├── api/
│       │   ├── auth.js
│       │   ├── runs.js
│       │   ├── servers.js
│       │   ├── tools.js
│       │   └── client.js
│       ├── components/           #пока не используется
│       │    ├── debug-panel.js
│       │    ├── loader.js
│       │    ├── modal.js
│       │    ├── navbar.js
│       │    └── debug-panel.js
│       ├── pages/
│       │   ├── login.js
│       │   ├── tools.js
│       │   ├── servers.js
│       │   └── runs.js
│       ├── router/
│       │   └── router.js
│       ├── state/               #пока не используется
│       │   ├── auth.js
│       │   ├── ui.js
│       │   └── debug.js
│       └── app.js
├── tools/
├── data/
│    └── servers.json
├── dev/
│    ├── ai_promt.md
│    ├── developer.md
│    └── bugs.txt
└── README.md

## Текущий принцип работы
Frontend
   ↓ 
REST API
   ↓
FastAPI Router
   ↓
Service Layer
   ↓
Tool Executor
   ↓
subprocess (tools/*.py)

## **Архитектурные принципы**
**Backend**
   API и бизнес-логика не смешиваются.
   Сложная логика выносится в services.
   Инструменты запускаются только через whitelist.
   Исключать command injection.
   Все изменения учитывать относительно будущей Run System.
Frontend
   app.js используется только как bootstrap.
   API вызовы находятся исключительно в js/api/.
   Экранная логика находится в js/pages/.
   Навигация осуществляется через router/router.js.
   Глобальное состояние хранится в js/state/.
   Новые страницы добавляются через pages + router.

## Реализовано
**Backend**:
   Авторизация
   Управление серверами
   Запуск инструментов через subprocess
   Whitelist инструментов
   Модульная backend-архитектура
**Frontend**:
   Полный рефакторинг frontend
   Разделение API/UI логики
   ES Modules
   SPA Router
   History API
   URL-маршруты
**Поддерживаемые маршруты:**
   /smoke
   /loading
   /stability
   /servers
   /runs
**Подготовлено**
   API слой для будущей Run System
   Страница Runs
   State слой
   Components слой
   Router слой

## Roadmap
### P1
- Перевести пользователей и токены в БД. Интеграция SQLite
- Добавить журнал запусков тестов.
- Добавить логирование.
- service/repository слой для работы с серверами
### P2
- SSE/WebSocket для онлайн-вывода логов.
- Очередь задач.
- Docker Compose.
- RBAC (роли пользователей).
### P3
- SSH-запуск тестов на удалённых серверах.
- Планировщик запусков.
- История и отчёты.
- Поддержка нескольких исполнителей-серверов тестов.
- Интеграция реальных инструментов НТ evi-utils
