# LoadStand
## Назначение проекта
LoadStand — платформа автоматизированного тестирования систем видеонаблюдения.
Основная бизнес-модель:
Node
→ Scenario
→ TestRun
→ Metrics
→ Result
→ Alert
→ Report

Система должна обеспечивать:
* управление серверами;
* удаленное выполнение тестов;
* генерацию видеонагрузки;
* генерацию API нагрузки;
* мониторинг инфраструктуры;
* мониторинг видеосервиса;
* анализ результатов;
* обнаружение инцидентов;
* формирование отчетов.

---

# Текущее состояние проекта
## Backend
* FastAPI
* Pydantic v2
* SQLAlchemy 2.x
* PostgreSQL
* Alembic
* Repository Pattern
* AsyncSSH
Реализовано:
* Run System (TestRun, RunStatus, RunResult, Migrations)
* Node Manager (Node, NodeRole, NodeStatus CRUD API)
* Auth API (Login/Logout)
* Runs API (History, Results)
* Nodes API (CRUD, Health Check, Bulk Check)
* SSH Executor (Async connections, pool, command execution)
* SSH Management API (Status, Reset)
* Node Health Check (Online/Offline tracking, Last Seen)
* SSH Connection Caching with invalidation on edit/delete

---

## Frontend
* Vanilla JS
* SPA Router с History API
* Fetch API client
Страницы:
* Smoke (tool execution)
* Loading (tool execution)
* Stability (tool execution)
* Runs (history table)
* Nodes (CRUD, health check, SSH status)
* SSH (command execution, status, reset)
Компоненты:
* Navbar (tabs, logout)
* Debug Panel
* Loader
* Modal
* Sidebar
Функции:
* Node auto-refresh (10s interval)
* SSH status refresh on tab switch/reload
* SSH connection reset button
* Status color indicators (green/red/yellow)
* Masked SSH credentials display
* Command polling (1s interval)

---

# Текущая архитектура
Backend:
Router
* Service
* Repository
* PostgreSQL
Frontend:
API
* Page
* Component
* UI

---

# Целевой стек
Backend:
* FastAPI
* AsyncSSH
* SQLAlchemy
* PostgreSQL
* TimescaleDB
* WebSocket
Frontend:
* Vanilla JS
* Chart.js
Monitoring:
* Prometheus
* Grafana
* Node Exporter

---

# Целевая архитектура
Node Manager
↓
SSH Executor
↓
Scenario Engine
↓
Test Orchestrator
↓
Metrics Manager
↓
Result Analyzer
↓
Alert Manager
↓
Report Generator

---

# Поддерживаемые роли узлов
* MEDIA_SERVER
* LOAD_SERVER
Будущие:
* ARCHIVE_SERVER
* ANALYTICS_SERVER

---

# Типы тестирования
## Устойчивость
Потоки:
* 20% WebRTC
* 10% Real Streams
* 70% Synthetic Streams
Контент:
* 10 типов видеоконтента
* H264
* H265
* 480p–4K
* 0.5–10 Mbps
## Архив
Проверка:
* постоянной записи
* записи по событию
## Отказоустойчивость
Сценарии:
* Restart Live
* Restart Database
## Камеры
Симуляция:
* Normal
* Limited Bandwidth
* Link Flapping
## API
Контроль:
* Latency
* Timeout
* 5xx Errors
* Regression
## Сверхнагрузка
Цель: Определение предельной производительности системы.
---

# Нагрузочные профили
* 100 Streams
* 500 Streams
* 1000 Streams
* Step Growth
* Avalanche
* Leak Test
* Mixed Clients
---

# Критерии успеха
* архив записывается без артефактов;
* live потоки без артефактов;
* CPU < 80%;
* равномерная загрузка CPU;
* отсутствие утечек RAM;
* контроль Load Average;
* количество активных потоков соответствует входящим;
* количество записей соответствует ожидаемому.

---

# Архитектурные правила
## Backend
Структура:
Router
→ Service
→ Repository
→ Database
Правила:
* Router отвечает только за HTTP.
* Service содержит бизнес-логику.
* Repository работает только с БД.
* Не использовать shell=True.
* Использовать whitelist запускаемых инструментов.

---

## Frontend
Структура:
api/
pages/
components/
router/
state/
Правила:
* fetch только внутри api/.
* app.js только bootstrap.
* бизнес-логика не размещается в UI.
* навигация только через router.
---

## Реализация новых сущностей
Обязательная цепочка:
Database
→ Repository
→ Service
→ Router
→ API
→ Frontend API
→ Page
→ UI
---

# Правила принятия решений
При реализации:
1. Сначала код.
2. Минимум объяснений.
3. Максимум готовых изменений файлов.
4. Не предлагать несколько вариантов без необходимости.
5. Учитывать целевую архитектуру.
Приоритет:
Код → Архитектура → Объяснение

---

# Завершённые этапы

## Этап 1: Run System ✓
* TestRun, RunStatus, RunResult модели
* PostgreSQL хранилище с Alembic миграциями
* Repository, Service, Router слои
* CRUD API
* Frontend таблица истории запусков
* Хранение stdout/stderr результатов

## Этап 2: Node Manager ✓
* Node, NodeRole, NodeStatus модели
* CRUD API с пагинацией и фильтрацией
* NodeRepository, NodeService слои
* Frontend CRUD UI (Create, Read, Update, Delete)
* SSH параметры хранение и маскирование
* Last Seen отслеживание

## Этап 3: SSH Executor ✓
* AsyncSSH с пулом соединений
* Кэширование по node.id с инвалидацией
* Async command execution с timeout
* stdout/stderr разделённый вывод
* Process monitoring и graceful stop
* SSH API endpoints

## Этап 4: Node Monitoring ✓
* SSH Health Check (/nodes/{id}/check и /nodes/check-all)
* Online/Offline status tracking
* SSH connection status (/ssh/{id}/status)
* SSH connection reset (/ssh/{id}/reset)
* Frontend UI с цветовыми индикаторами (зеленый/красный)
* Auto-refresh на смену ноды, возврат на таб, pageshow
* Cache invalidation при редактировании SSH параметров
* Batch check всех нод с ошибкой-handling

---

# Правило завершения этапов
Этап считается завершенным только если реализованы:
1. Data Layer
2. Repository Layer
3. Business Layer
4. API Layer
5. Frontend Layer
6. UI Layer
Если отсутствует хотя бы один уровень, статус = IN PROGRESS
