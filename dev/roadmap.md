# Roadmap LoadStand

## Этап 1. Run System
Цель: Ввести модель тестовых запусков.
Реализовано:
* TestRun
* RunStatus
* RunResult
* PostgreSQL
* SQLAlchemy
* Alembic
* история запусков
* хранение результатов
* Web UI результатов

Результат:
Tool → TestRun → RunResult
Статус: COMPLETED
---

## Этап 2. Node Manager
Цель: Управление инфраструктурными узлами.
Реализовано:
* Node
* NodeRole
* NodeStatus
* NodeRepository
* NodeService
* PostgreSQL хранение
* CRUD API
* CRUD UI
* Last Seen
* Health Check
Поддерживаемые роли:
* MEDIA_SERVER
* LOAD_SERVER

Результат:
Node → CRUD → UI
Статус: COMPLETED

---

## Этап 3. SSH Executor
Цель: Удаленное выполнение команд.
Реализовать:
* AsyncSSH
* SSH Pool
* Execute Command
* Stop Command
* stdout
* stderr
Результат:
Node → SSH Executor
Статус: PLANNED

---

## Этап 4. Node Monitoring
Цель: Мониторинг доступности узлов.
Реализовать:
* SSH Health Check
* Online/Offline
* Last Seen Update
* Auto Refresh

Результат:
Node → Health
Статус: PLANNED

---

## Этап 5. Live Logs
Цель: Отображение выполнения в реальном времени.
Реализовать:
* WebSocket
* Streaming Logs
* Run Status Updates
* Progress Updates

Результат:
Run → Live Logs → UI

Статус: PLANNED

---

## Этап 6. Load Profiles
Цель: Стандартизировать нагрузку.
Реализовать:
* LoadProfile
* 100 Streams
* 500 Streams
* 1000 Streams
* Custom Profiles

Результат:
LoadProfile → Run

Статус: PLANNED

---

## Этап 7. Traffic Generator
Цель: Генерация видеопотоков.
Реализовать:
* MediaMTX Integration
* RTSP Streams
* WebRTC Streams
* Synthetic Streams
* Mixed Streams

Результат:
Profile → Traffic

Статус: PLANNED

---

## Этап 8. API Load Generator
Цель: Нагрузка на API видеосервиса.
Реализовать:
* GET Load
* POST Load
* Latency Metrics
* Error Rate Metrics
* Baseline Measurement

Результат:
Profile → API Load

Статус: PLANNED

---

## Этап 9. Scenario Engine
Цель: Оркестрация тестов.
Реализовать:
* Scenario
* ScenarioStep
* ScenarioParameter
* Scenario Runner

Результат:
Scenario → Run

Статус: PLANNED

---

## Этап 10. Failure Injection
Цель: Проверка отказоустойчивости.
Реализовать:
* Service Restart
* Database Restart
* Link Flapping
* Bandwidth Limiting

Результат:
Scenario → Failure Test

Статус: PLANNED

---

## Этап 11. Infrastructure Metrics
Цель: Сбор инфраструктурных метрик.
Реализовать:
* CPU
* RAM
* Disk
* Disk IO
* Network IO
* Load Average

Результат:
Node → Metrics

Статус: PLANNED

---

## Этап 12. Video Metrics
Цель: Сбор метрик видеосервиса.
Реализовать:
* Active Streams
* FPS
* Bitrate
* Reconnects
* Frame Loss
* Recording Count

Результат:
Video → Metrics

Статус: PLANNED

---

## Этап 13. Historical Metrics Storage
Цель: Долговременное хранение метрик.
Реализовать:
* TimescaleDB
* Aggregation
* Retention Policies
* Run Comparison

Результат:
Metrics → History

Статус: PLANNED

---

## Этап 14. Result Analyzer
Цель: Автоматическая оценка результатов.
Реализовать:
* PASS
* WARNING
* FAIL
* Success Rules
* Regression Detection

Результат:
Metrics → Result

Статус: PLANNED

---

## Этап 15. Alert Manager
Цель: Уведомления об инцидентах.
Реализовать:
* Event
* Alert
* Telegram
* Email

Результат:
Result → Alert

Статус: PLANNED

---

## Этап 16. Report Generator
Цель: Формирование отчетов.
Реализовать:
* HTML Reports
* PDF Reports
* Metrics Summary
* Comparison Reports

Результат:
Run → Report

Статус: PLANNED

---

## Этап 17. Production Ready
Реализовать:
* Docker Compose
* Nginx
* HTTPS
* RBAC
* Backup
* Prometheus
* Grafana
* CI/CD

Статус: PLANNED
