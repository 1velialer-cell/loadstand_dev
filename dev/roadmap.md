# Roadmap LoadStand

## Этап 1. Run System
Цель: Перейти от запуска инструментов к полноценным тестовым запускам.

Реализовано:
* TestRun
* RunStatus
* RunResult
* PostgreSQL
* SQLAlchemy
* Alembic
* хранение запусков
* хранение результатов
* история запусков
* отображение результатов в Web UI

Результат:
Tool → Run → Result

Статус: COMPLETED

---

## Этап 2. Node Manager
Цель: Ввести доменную сущность Node и централизованное управление узлами выполнения.

Реализовано:
* Node
* NodeRole
* NodeRepository
* NodeService
* PostgreSQL хранение узлов
* CRUD API для Nodes
* Web UI управления Nodes
* Node Status
* Node Check API
* перенос хранения Nodes из JSON в PostgreSQL

В работе:
* Last Seen
* Health Check логика
* автоматическое обновление статусов
* очистка legacy Servers

Поддерживаемые роли:
* MEDIA_SERVER
* LOAD_SERVER

Результат:
Node → Run

Статус: IN_PROGRESS

---

## Этап 3. SSH Executor
Цель: Выполнение тестов на удалённых узлах.

Реализовать:
* AsyncSSH
* SSH Connection Pool
* удалённое выполнение команд
* остановку процессов
* получение stdout/stderr
* загрузку файлов
* проверку доступности узлов через SSH

Результат:
Run
→ SSH Executor
→ Node

Статус: PLANNED

---

## Этап 4. Distributed Run Engine
Цель: Запуск тестов непосредственно на Nodes.

Реализовать:
* назначение Run на Node
* выбор Node по роли
* очередь выполнения
* контроль статусов выполнения
* распределение нагрузки между Nodes
* отмену запуска

Результат:
Run
→ Node
→ Execution

Статус: PLANNED

---

## Этап 5. Live Logs
Реализовать:
* WebSocket
* потоковую передачу логов
* отображение статуса выполнения
* отображение прогресса запуска
* уведомления о завершении
* просмотр логов в реальном времени

Результат:
Run
→ Live Logs
→ Web UI

Статус: PLANNED

---

## Этап 6. Scenario Engine
Реализовать:
* Scenario
* ScenarioStep
* ScenarioParameter
* выполнение сценариев
* условия выполнения
* повторное использование сценариев

Типовой сценарий:

Подготовка
↓
Запуск RTSP
↓
Подключение
↓
Нагрузка
↓
Сбор результатов
↓
Отчет

Результат:
Scenario
→ Run

Статус: PLANNED

---

## Этап 7. Metrics Manager
Цель: Сбор инфраструктурных и прикладных метрик.

Infrastructure:
* CPU
* RAM
* Disk Usage
* Disk IO
* Network IO
* Load Average

Video:
* FPS
* Bitrate
* Streams
* Frame Loss
* Reconnects

Service:
* Active Streams
* Camera Count
* Processing Queues

Archive:
* Write Speed
* Queue Size
* Disk Space

Результат:
Run
→ Metrics

Статус: PLANNED

---

## Этап 8. Historical Metrics Storage
Реализовать:
* TimescaleDB
* хранение временных рядов
* сравнение запусков
* агрегирование данных
* долгосрочное хранение
* базовую аналитику

Результат:
Metrics
→ History

Статус: PLANNED

---

## Этап 9. Result Analyzer
Реализовать:
* критерии успешности
* эталонные профили
* PASS
* WARNING
* FAIL
* автоматическую оценку результатов
* сравнение с предыдущими запусками

Результат:
Metrics
→ Result

Статус: PLANNED

---

## Этап 10. Alert Manager
Реализовать:
* Event
* Alert
* правила обнаружения инцидентов
* Telegram уведомления
* Email уведомления
* журнал событий

Результат:
Result
→ Alert

Статус: PLANNED

---

## Этап 11. Reports
Реализовать:
* Report
* генерацию отчетов
* HTML отчеты
* PDF отчеты
* экспорт результатов
* сравнительные отчеты
* экспорт метрик

Результат:
Run
→ Report

Статус: PLANNED

---

## Этап 12. Production Ready
Реализовать:
* Docker Compose
* Nginx
* HTTPS
* RBAC
* аудит действий
* резервное копирование
* Grafana
* Prometheus
* CI/CD
* мониторинг системы

Результат:
Production Deployment

Статус: PLANNED