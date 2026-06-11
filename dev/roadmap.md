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
Цель: Ввести доменную сущность Node.
Реализовать:
* Node
* NodeRole
* NodeRepository
* NodeService
* PostgreSQL хранение узлов
* перенос Servers из JSON в PostgreSQL
* проверку доступности узлов
* Last Seen
* состояние узла
Поддерживаемые роли:
* MEDIA_SERVER
* LOAD_SERVER
Результат:
Node→ Run
Статус: PLANNED
---

## Этап 3. SSH Executor
Реализовать:
* AsyncSSH
* SSH Connection Pool
* удаленное выполнение команд
* остановку процессов
* получение stdout/stderr
* проверку доступности узлов
Результат:
Run
→ SSH Executor
→ Node
Статус: PLANNED
---

## Этап 4. Live Logs
Реализовать:
* WebSocket
* потоковую передачу логов
* отображение статуса выполнения
* отображение прогресса запуска
* уведомления о завершении
Результат:
Run
→ Live Logs
→ Web UI
Статус: PLANNED
---

## Этап 5. Scenario Engine
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

## Этап 6. Metrics Manager
Реализовать сбор метрик.
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

## Этап 7. Historical Metrics Storage
Реализовать:
* TimescaleDB или VictoriaMetrics
* хранение временных рядов
* сравнение запусков
* агрегирование данных
* долгосрочное хранение
Результат:
Metrics
→ History
Статус: PLANNED
---

## Этап 8. Result Analyzer
Реализовать:
* критерии успешности
* эталонные профили
* PASS
* WARNING
* FAIL
* автоматическую оценку результатов
Результат:
Metrics
→ Result
Статус: PLANNED
---

## Этап 9. Alert Manager
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

## Этап 10. Reports
Реализовать:
* Report
* генерацию отчетов
* HTML отчеты
* PDF отчеты
* экспорт результатов
* сравнительные отчеты
Результат:
Run → Report
Статус: PLANNED
---
## Этап 11. Production Ready
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
Статус: PLANNED
