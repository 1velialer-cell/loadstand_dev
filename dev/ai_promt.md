# LoadStand
## Назначение проекта
LoadStand — платформа автоматизированного нагрузочного тестирования систем видеонаблюдения.
Основная задача системы — проведение автоматизированных испытаний полного конвейера обработки видеопотоков:
RTSP Generator
→ Video Service
→ Motion Detector
→ Archive
Система должна обеспечивать:
* управление инфраструктурными узлами;
* выполнение сценариев испытаний;
* запуск и контроль тестов;
* мониторинг инфраструктуры;
* мониторинг видеопотоков;
* сбор и хранение метрик;
* анализ результатов;
* обнаружение аварийных ситуаций;
* формирование отчетов.
---

# Текущее состояние проекта
Проект находится на стадии MVP.
Реализовано:
Backend:
* FastAPI
* Pydantic
* AsyncIO
* Token Authentication
* запуск инструментов через subprocess
* whitelist разрешенных инструментов
* модульная архитектура Router → Service
Frontend:
* Vanilla JS (ES Modules)
* SPA Router
* History API
* страницы:
  * Smoke
  * Loading
  * Stability
  * Servers
  * Runs
Отсутствует:
* PostgreSQL
* SQLAlchemy
* Alembic
* история запусков
* SSH Executor
* Node Manager
* Scenario Engine
* Metrics Manager
* Result Analyzer
* Alert Manager
* Live Logs
* система отчетности

На текущем этапе система фактически выполняет роль интерфейса запуска тестовых инструментов.
---

# Целевая архитектура
Frontend SPA
▼
FastAPI Backend
┌────┼─────────────────────────────┐
▼    ▼                             ▼
Node Manager
Scenario Engine
Metrics Manager
  ▼
Test Orchestrator
  ▼
Result Analyzer
  ▼
Alert Manager
---

# Основные доменные сущности
## Infrastructure
Node
NodeRole
Поддерживаемые роли:
MEDIA_SERVER
LOAD_SERVER
Будущие роли:
ARCHIVE_SERVER
ANALYTICS_SERVER
GPU_SERVER
---

## Scenarios
Scenario
ScenarioStep
ScenarioParameter
---
## Runs
TestRun
RunStatus:
CREATED
PREPARING
RUNNING
STOPPING
FINISHED
FAILED
RunResult
---
## Metrics
Metric
MetricSeries
MetricSnapshot
---
## Events
Event
Alert
AlertSeverity:
INFO
WARNING
CRITICAL
---
## Reports
Report
---

# Мониторинг инфраструктуры
Для каждого узла должны собираться:
* CPU
* RAM
* Disk Usage
* Disk IO
* Network IO
* Load Average
---

# Мониторинг видеопотоков
Основные показатели:
* количество RTSP потоков
* количество подключенных потоков
* количество потерянных потоков
* количество переподключений
* FPS
* битрейт
* задержка подключения
---

# Мониторинг видеосервиса
Контролируются:
* количество камер
* количество активных потоков
* количество ошибок подключения
* время обработки потока
* очереди обработки
---

# Мониторинг детектора движения
Контролируются:
* скорость обработки кадров
* количество обработанных кадров
* количество пропущенных кадров
* количество событий движения
* загрузка CPU/GPU
---

# Мониторинг архива
Контролируются:
* скорость записи
* объем данных
* очередь записи
* ошибки записи
* свободное место на диске
---

# Архитектурные правила Backend
Слои:
Router
→ Service
→ Repository
→ Storage

Правила:
* Router отвечает только за HTTP.
* Бизнес-логика размещается только в Service.
* Работа с БД выполняется через Repository.
* Storage не используется напрямую из Router.
* Исключать command injection.
* Использовать whitelist инструментов.
* Не использовать shell=True.

---
# Архитектурные правила Frontend
Frontend реализован как SPA.
Структура ответственности:
api/ - работа с backend
pages/ - экранная логика
router/ - маршрутизация
state/ - состояние приложения
components/ - UI-компоненты
app.js - только bootstrap
Запрещено:
* fetch внутри pages
* бизнес-логика в app.js
* обход router
* смешивание API и UI
---

# Архитектурный приоритет
Главная бизнес-модель системы:
Node
→ Scenario
→ Run
→ Metrics
→ Result
→ Alert
Любая новая функциональность должна проектироваться относительно этой цепочки.
---

# Правила принятия решений
Перед реализацией анализировать влияние изменений на:
* Test Orchestrator
* Node Manager
* Scenario Engine
* Metrics Manager
* Result Analyzer
* Alert Manager
* историю запусков
* SSH Executor
* масштабирование системы
Если решение создает технический долг относительно целевой архитектуры — необходимо явно указать это до реализации.
---

# Технологический стек
Backend:
* FastAPI
* Pydantic
* AsyncIO
Планируемо:
* AsyncSSH
* SQLAlchemy
* PostgreSQL
* Alembic
Frontend:
* Vanilla JS
* HTML
* CSS
* SPA Router
Планируемо:
* Chart.js или Apache ECharts
Мониторинг:
* Prometheus
* Grafana
* TimescaleDB или VictoriaMetrics

# Текущая архитектура проекта
loadstand/
├── main.py
├── backend/
├── core/
│   ├── config.py
│   └── sec.py
├── models/
│   └── schemas.py
├── routers/
│   ├── auth.py
│   ├── tools.py
│   ├── logo.py
│   └── servers.py
├── services/
│   └── tool_executor.py
└── storage.py
├── frontend/
├── index.html
├── styles.css
└── js/
├── api/
│   ├── client.js
│   ├── auth.js
│   ├── tools.js
│   ├── servers.js
│   └── runs.js
├── pages/
│   ├── login.js
│   ├── tools.js
│   ├── servers.js
│   └── runs.js
├── router/
│   └── router.js
├── state/
│   ├── auth.js
│   ├── ui.js
│   └── debug.js
├── components/
│   ├── modal.js
│   ├── navbar.js
│   ├── loader.js
│   └── debug-panel.js
└── app.js
├── tools/
├── data/
│   └── servers.json
├── dev/
│   ├── project_context.md
│   ├── roadmap.md
│   └── bugs.txt
└── README.md

# Слои ответственности текущей архитектуры проекта
backend/routers - HTTP API слой.
backend/services - Бизнес-логика.
backend/modelsDTO - Pydantic схемы.
backend/storage - Временное хранилище MVP.
frontend/js/api - Работа с backend API.
frontend/js/pages - Экранная логика.
frontend/js/router - SPA навигация.
frontend/js/state - Глобальное состояние приложения.
frontend/js/components - Переиспользуемые UI-компоненты.
frontend/js/app.js - Только bootstrap приложения.

# Целевая архитектура проекта
loadstand/
├── backend/
├── core/
├── models/
├── routers/
│   ├── auth.py
│   ├── nodes.py
│   ├── scenarios.py
│   ├── runs.py
│   ├── metrics.py
│   ├── alerts.py
│   └── reports.py
├── services/
│   ├── node_manager/
│   ├── scenario_engine/
│   ├── test_orchestrator/
│   ├── metrics_manager/
│   ├── result_analyzer/
│   ├── alert_manager/
│   └── ssh_executor/
├── repositories/
│   ├── node_repository.py
│   ├── scenario_repository.py
│   ├── run_repository.py
│   ├── metric_repository.py
│   ├── alert_repository.py
│   └── report_repository.py
├── db/
│   ├── models/
│   ├── migrations/
│   └── session.py
└── websocket/
│   ├── logs.py
│   ├── metrics.py
│   └── alerts.py
├── frontend/
├── pages/
│   ├── dashboard
│   ├── nodes
│   ├── scenarios
│   ├── runs
│   ├── metrics
│   ├── alerts
│   └── reports
├── charts/
├── state/
└── components/

# Слои ответственности целевой архитектуры проекта
MVP Architecture
Tool
→ Subprocess
→ Result
Target Architecture
Node
→ Scenario
→ TestRun
→ Metrics
→ Result Analysis
→ Alerting
Любые новые изменения должны приближать проект к Target Architecture.
Запрещено принимать решения, которые усложняют переход к:
* PostgreSQL
* SSH Executor
* Node Manager
* Scenario Engine
* Metrics Manager
* Result Analyzer
* Alert Manager
* Historical Metrics Storage
