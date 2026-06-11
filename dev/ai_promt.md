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
Проект завершил этап Run System.
Реализовано:
Backend:
  FastAPI
  Pydantic
  AsyncIO
  PostgreSQL
  SQLAlchemy
  Alembic
  Repository Layer
  RunService
  RunRepository
  RunResultRepository
  Token Authentication
  запуск инструментов через subprocess
  whitelist разрешенных инструментов
Frontend:
  Vanilla JS (ES Modules)
  SPA Router
  History API
Страницы:
  Smoke
  Loading
  Stability
  Servers
  Runs
Run System:
  TestRun
  RunStatus
  RunResult
  хранение запусков
  хранение результатов
  история запусков
  отображение результатов
Отсутствует:
  SSH Executor
  Node Manager
  Scenario Engine
  Metrics Manager
  Result Analyzer
  Alert Manager
  Reports
  Live Logs
На текущем этапе система реализует полноценную модель тестовых запусков:
Tool → TestRun → RunResult
Все запуски и результаты сохраняются в PostgreSQL.
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
→ TestRun
→ Metrics
→ Result
→ Alert
→ Report
Текущая реализованная часть модели:
Tool
→ TestRun
→ RunResult
Любая новая функциональность должна проектироваться относительно полной целевой цепочки.
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

# Правило реализации функциональности
Каждый этап roadmap должен реализовываться сквозным образом.
Обязательно проектировать одновременно:
* Backend
* API
* Frontend
* UI
Функциональность не считается завершенной, если реализован только Backend.
Минимальный критерий завершения этапа:
Backend:
* модели
* сервисы
* репозитории
* API
Frontend:
* API слой
* страницы
* состояние приложения
* UI компоненты
UI:
* отображение данных
* взаимодействие пользователя
* обработка ошибок
* обновление состояния
Любая новая сущность должна проходить полный путь:
Database
→ Repository
→ Service
→ Router
→ API
→ Frontend API
→ Page
→ UI
Например:
Node
→ NodeRepository
→ NodeService
→ NodesRouter
→ /api/nodes
→ frontend/api/nodes.js
→ frontend/pages/nodes.js
→ UI Nodes Page
Scenario
→ ScenarioRepository
→ ScenarioService
→ ScenariosRouter
→ /api/scenarios
→ frontend/api/scenarios.js
→ frontend/pages/scenarios.js
→ UI Scenarios Page
Metrics
→ MetricRepository
→ MetricsService
→ MetricsRouter
→ /api/metrics
→ frontend/api/metrics.js
→ frontend/pages/metrics.js
→ UI Metrics Dashboard
Запрещено считать этап выполненным, если данные доступны только через API или только через БД.
Результат каждой реализации должен быть доступен пользователю через Web UI.
Run System считается завершенным.
Запрещено проектировать новую функциональность через прямой вызов Tool Executor из Router.
Все новые механизмы запуска должны строиться через:
TestRun
→ Service
→ Executor
а не через:
Router
→ Subprocess
Любое решение должно учитывать будущий переход к:
Node
→ SSH Executor
→ Scenario Engine
Текущий технический долг:
Tool API все еще существует параллельно с Run API.
Run выполняется синхронно внутри HTTP запроса.
Live Logs отсутствуют.
Node Manager отсутствует.
SSH Executor отсутствует.
Указанные ограничения необходимо учитывать при проектировании новых модулей.
---

# Правило завершения этапов
Этап roadmap считается завершенным только если выполнены все уровни:
1. Data Layer
2. Business Layer
3. API Layer
4. Frontend Layer
5. UI Layer
Если отсутствует хотя бы один уровень, этап имеет статус IN PROGRESS.

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
├── db/
├── models/
├── routers/
│ ├── auth.py
│ ├── runs.py
│ ├── nodes.py
│ ├── scenarios.py
│ ├── metrics.py
│ ├── alerts.py
│ └── reports.py
├── services/
│ ├── run_service.py
│ ├── node_manager/
│ ├── ssh_executor/
│ ├── scenario_engine/
│ ├── metrics_manager/
│ ├── result_analyzer/
│ └── alert_manager/
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

