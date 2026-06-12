# LoadStand
## 1. Назначение проекта

LoadStand — платформа автоматизированного нагрузочного тестирования систем видеонаблюдения.
Основная целевая цепочка:
Node
→ Scenario
→ TestRun
→ Metrics
→ Result
→ Alert
→ Report

Система должна обеспечивать:
- управление инфраструктурными узлами;
- выполнение тестовых сценариев;
- запуск и контроль нагрузочных тестов;
- мониторинг инфраструктуры;
- мониторинг видеосервисов;
- сбор и хранение метрик;
- анализ результатов;
- обнаружение инцидентов;
- формирование отчетов.

---

# 2. Текущее состояние проекта
## Стек
### Backend
- FastAPI
- Pydantic v2
- SQLAlchemy 2.x
- PostgreSQL
- Alembic
- AsyncIO

### Frontend
- Vanilla JS (ES Modules)
- SPA Router
- History API
- HTML
- CSS

## Реализовано
### Run System
- TestRun
- RunStatus
- RunResult
- хранение запусков
- хранение результатов
- история запусков
- отображение результатов
### Node Manager
- Node
- NodeRole
- NodeStatus
- NodeRepository
- NodeService
- PostgreSQL хранение узлов
- CRUD API
- Web UI управления узлами
- проверка доступности узлов
- Last Seen
- состояние узлов
### API
- Auth API
- Runs API
- Nodes API

### Frontend
Страницы:
- Smoke
- Loading
- Stability
- Runs
- Nodes
## Текущая бизнес-модель
Tool
→ TestRun
→ RunResult
Node
→ TestRun
---

# 3. Текущая архитектура проекта
## Backend
Router → Service → Repository → PostgreSQL
### Ответственность слоев
#### Router
Только HTTP:
- request
- response
- validation
- dependency injection

#### Service
Бизнес-логика:
- правила системы
- orchestration
- проверки

#### Repository
Работа с БД:
- CRUD
- запросы
- выборки

#### Database
Хранение данных.

---

## Frontend
api/
→ pages/
→ components/
→ router/

### Ответственность
#### api/
Только работа с backend API.
#### pages/
Экранная логика.
#### components/
Переиспользуемые UI-компоненты.
#### router/
SPA маршрутизация.
#### app.js
Только bootstrap приложения.

---

# 4. Целевой стек
## Backend
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Alembic
- AsyncSSH
- WebSocket
## Frontend
- Vanilla JS
- SPA Router
- Chart.js или Apache ECharts
## Monitoring
- Prometheus
- Grafana
## Metrics Storage
- TimescaleDB или VictoriaMetrics
---

# 5. Целевая архитектура проекта
## Backend
Node Manager
↓
Scenario Engine
↓
Test Orchestrator
↓
SSH Executor
↓
Metrics Manager
↓
Result Analyzer
↓
Alert Manager
↓
Report Generator

---

## Целевая бизнес-модель
Node
→ Scenario
→ TestRun
→ Metrics
→ Result
→ Alert
→ Report
---

## Основные сущности
### Infrastructure
- Node
- NodeRole
- NodeStatus
### Scenarios
- Scenario
- ScenarioStep
- ScenarioParameter
### Runs
- TestRun
- RunResult
### Metrics
- Metric
- MetricSnapshot
- MetricSeries
### Events
- Event
- Alert
### Reports
- Report

---

# 6. ИНФОРМАЦИЯ ДЛЯ ИИ
## 6.1 Архитектурные правила
### Backend
Обязательная структура:
Router
→ Service
→ Repository
→ Database
Правила:
- Router не содержит бизнес-логики.
- Service не работает напрямую с HTTP.
- Repository работает только с БД.
- SQL не размещается в Router.
- Бизнес-логика не размещается в Repository.
- Любая новая сущность должна иметь:
  - Model
  - Repository
  - Service
  - Router
  - API
---
### Frontend
Обязательная структура:
API
→ Page
→ UI
Правила:
- fetch только внутри api/.
- страницы не обращаются напрямую к backend.
- app.js содержит только bootstrap.
- маршрутизация только через router.
- UI не содержит бизнес-логики.
---
### Database
Правила:
- PostgreSQL является единственным источником данных.
- Использовать Alembic для всех изменений схемы.
- Не хранить доменные данные в JSON-файлах.
- Все сущности должны иметь миграции.
---
### UI
Правила:
- Каждая сущность должна иметь интерфейс управления.
- Данные должны быть доступны пользователю через Web UI.
- API без UI не считается завершенной реализацией.
---
## 6.2 Правила принятия решений
При реализации:
1. Сначала писать код.
2. Объяснения минимальные.
3. Не предлагать несколько вариантов без необходимости.
4. Давать готовые изменения файлов.
5. Показывать конкретные патчи и код.
6. Избегать абстрактных рассуждений.
7. Если найден архитектурный долг — указать одной короткой секцией.

Приоритет:
Код → Архитектура → Объяснение
а не наоборот.

---

## 6.3 Правило завершения этапов
Этап считается завершенным только если реализованы все уровни:
### Data Layer
- модели БД
- миграции
### Repository Layer
- CRUD
- запросы
### Business Layer
- сервисы
- бизнес-логика
### API Layer
- роуты
- схемы
### Frontend Layer
- API клиент
- страницы
### UI Layer
- отображение
- управление
- обработка ошибок

Обязательная цепочка реализации:
Database → Repository → Service → Router → API → Frontend API → Page → UI
Если отсутствует хотя бы один уровень — этап имеет статус: IN PROGRESS а не COMPLETED.