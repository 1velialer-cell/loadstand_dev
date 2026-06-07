# Roadmap LoadStand

## Этап 1. Run System
Цель: Перейти от запуска инструментов к полноценным тестовым запускам.
Реализовать:
* TestRun
* RunStatus
* RunResult
* PostgreSQL
* SQLAlchemy
* Alembic
* хранение запусков
* хранение результатов
Результат: Tool → Run → Result
Статус: IN PROGRESS
---

## Этап 2. Live Logs
Реализовать:
* WebSocket или SSE
* потоковую передачу логов
* отображение статуса выполнения
* уведомления о завершении
Статус: PLANNED
---

## Этап 3. SSH Executor
Реализовать:
* AsyncSSH
* SSH Connection Pool
* запуск процессов на удаленных серверах
* остановку процессов
* получение логов
Результат: Run → SSH Executor → Remote Server
Статус: PLANNED
---

## Этап 4. Node Manager
Реализовать:
* регистрацию узлов
* роли серверов
* хранение конфигурации
* проверку доступности
Поддерживаемые роли:
* MEDIA_SERVER
* LOAD_SERVER
Статус: PLANNED
---

## Этап 5. Scenario Engine
Реализовать:
* сценарии испытаний
* шаги сценариев
* параметры сценариев
* условия выполнения
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
Статус: PLANNED
---

## Этап 6. Metrics Manager
Реализовать сбор:
Infrastructure:
* CPU
* RAM
* Disk
* Network
Video:
* FPS
* Bitrate
* Streams
* Frame Loss
Статус: PLANNED
---

## Этап 7. Historical Metrics Storage
Реализовать:
* TimescaleDB или VictoriaMetrics
* хранение временных рядов
* сравнение тестовых запусков
Статус: PLANNED
---

## Этап 8. Result Analyzer
Реализовать:
* критерии успешности
* эталонные профили
* PASS
* WARNING
* FAIL
Статус: PLANNED
---

## Этап 9. Alert Manager
Реализовать:
* правила обнаружения инцидентов
* Telegram уведомления
* Email уведомления
* журнал событий
Статус: PLANNED
---

## Этап 10. Production Ready
Реализовать:
* Docker Compose
* Nginx
* HTTPS
* RBAC
* аудит действий
* резервное копирование
* Grafana
* Prometheus
Статус: PLANNED
 
 