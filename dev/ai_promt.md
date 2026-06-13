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
Реализовано:
* Run System
* Node Manager
* Auth API
* Runs API
* Nodes API
* SSH Executor
* Node Health Check

---

## Frontend
* Vanilla JS
* SPA Router
* History API
Страницы:
* Smoke
* Loading
* Stability
* Runs
* Nodes
* SSH

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

# Правило завершения этапов
Этап считается завершенным только если реализованы:
1. Data Layer
2. Repository Layer
3. Business Layer
4. API Layer
5. Frontend Layer
6. UI Layer
Если отсутствует хотя бы один уровень, статус = IN PROGRESS
