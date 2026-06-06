## Общая информация
**Loadstand** — веб-система автоматизации запуска smoke, load и stability тестов.
**Цель:** Упростить и стандартизировать процесс запуска тестовых скриптов через удобный веб-интерфейс с возможностью дальнейшего масштабирования на несколько серверов.

## Текущий технологический стек
- **Backend**: FastAPI + Uvicorn
- Модульная структура backend (`routers`, `services`, `models`, `core`)
- **Frontend**: Vanilla JavaScript + HTML + CSS (без фреймворков)
- **Выполнение тестов**: `asyncio.create_subprocess_exec`
- **Авторизация**: Простая token-based (in-memory)
- **Язык**: Python 3.10+
- **Отладка**: Прямой запуск на сервере

## Текущая архитектура
loadstand/
├── main.py
├── backend/
│   ├── core/
│   │   ├── config.py
│   │   └── sec.py
│   ├── models/
│   │   └── schemas.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── tools.py
│   │   ├── logo.py
│   │   └── servers.py
│   ├── services/
│   │   └── tool_executor.py
│   └── storage.py
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── tools/
├── data/
│   └── servers.json
├── dev/
└── README.md

**Как работает:**
Frontend → REST API (FastAPI) → Tool Executor → subprocess (python3 tools/xxx.py)

## Анализ стека и архитектуры
### Плюсы:
- Простота и минимализм
- Быстрый запуск и разработка
- FastAPI — современный и производительный
- Нет тяжёлых зависимостей
- Хорошая основа для MVP
### Минусы и проблемы:
- **Frontend** плоский и содержит дублирование логики
- **Отсутствует** поддержка удалённых серверов
- **Нет** логов, истории запусков, реального времени вывода
- **Авторизация** хранится в памяти (не persistent)
- **Нет** обработки длинных задач (long-running tasks)

## Планируемая структура проекта
/loadstand/
├── main.py                    # только запуск приложения
├── config.py                  # настройки, пути, timeouts
├── requirements.txt
├── README.md
├── DEVELOPER.md
backend/
├── core/
│   ├── config.py
│   ├── security.py
│   └── logging.py
├── routers/
├── services/
│   ├── tool_executor.py
│   ├── auth_service.py
│   └── server_service.py
├── repositories/
│   ├── users_repository.py
│   └── servers_repository.py
├── models/
└── tasks/
frontend/
├── js/
│   ├── api.js
│   ├── auth.js
│   ├── tabs.js
│   ├── tools.js
│   └── servers.js
├── logo.svg
├── app.js
├── styles.css
└── index.html
├── tools/
│   ├── smoke-test.py
│   ├── load-test.py
│   └── stability-test.py
├── dev/                      
│   ├── ai_promt.md            # промт для ввода ИИ в контекст 
│   ├── bugs.md                # запись багов для фикса во время dev
│   └── project.md             # dev-документация
└── logs/                      

## Roadmap
### Технический долг
#### Backend
1. `storage.py` хранит пользователей и токены в памяти.
   - Потеря данных после рестарта.
   - Не подходит для нескольких экземпляров приложения.
2. Логика серверов хранится прямо в router.
   - Функции `read_servers/write_servers` необходимо вынести в сервис.
3. Нет слоя репозиториев.
   - Работа с файлами смешана с API.
4. Нет централизованного логирования.
5. Нет обработки фоновых задач.
   - Долгие тесты будут блокировать пользовательские сценарии.
#### Frontend
1. `app.js` стал монолитным.
2. Работа с API, авторизацией, вкладками и серверами смешана.
3. Нет модульности.
4. Нет механизма обновления статуса выполнения теста в реальном времени.

## Критичные улучшения
### Приоритет P1
- Перевести пользователей и токены в БД.
- Добавить журнал запусков тестов.
- Добавить логирование.
- Вынести работу с серверами в service/repository слой.
### Приоритет P2
- SSE/WebSocket для онлайн-вывода логов.
- Очередь задач.
- Docker Compose.
- Переезд на микросервисную структуру (`routers/`, `services/`)
- RBAC (роли пользователей).
### Приоритет P3
- SSH-запуск тестов на удалённых серверах.
- Планировщик запусков.
- Подключение реальных инструментов НТ evi-utils
- История и отчёты.
- Поддержка нескольких исполнителей тестов.
