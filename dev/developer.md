## Общая информация
**Loadstand** — веб-система автоматизации запуска smoke, load и stability тестов.
**Цель:** Упростить и стандартизировать процесс запуска тестовых скриптов через удобный веб-интерфейс с возможностью дальнейшего масштабирования на несколько серверов.

## Текущий технологический стек
- **Backend**: FastAPI + Uvicorn
- **Frontend**: Vanilla JavaScript + HTML + CSS (без фреймворков)
- **Выполнение тестов**: `asyncio.create_subprocess_exec`
- **Авторизация**: Простая token-based (in-memory)
- **Язык**: Python 3.10+
- **Отладка**: Прямой запуск на сервере

## Текущая архитектура
/loadstand/
├── main.py                    # Запуск
├── backend/                   
│   ├── api.py                 # API
│   ├── auth.py                # Авторизация
│   ├── start.py               # Запуск тестов из /tools
│   └── storage.py             # Запись пользователей
├── frontend/                  
│   ├── index.html             # Верстка 
│   ├── styles.css             # Стиль для верстки
│   └── app.js                 # Основная логика frontend
├── tools/                     
│   ├── smoke-test.py          # скрипт для смок-теста (пока заглушка)
│   ├── load-test.py           # скрипт для нагрузочного-теста (пока заглушка)
│   └── stability-test.py      # скрипт для стабильного-теста (пока заглушка)
├── dev/                      
│   ├── ai_promt.md            # промт для ввода ИИ в контекст 
│   ├── bugs.md                # запись багов для фикса во время dev
│   └── project.md             # dev-документация
└── README.md                  # user-документация

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
- **Структура**: Всё свалено в кучу (`start.py`, `api.py`, `main.py`)
- **Отсутствие** `config.py` и `.env`
- **Нет** разделения на `routers/`, `services/`, `core/`
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
├── logo.svg
├── backend/
│   ├── __init__.py
│   ├── core/                  # конфиги, security, exceptions
│   ├── routers/               # api.py → routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── tools.py           # бывший start.py
│   │   └── status.py
│   ├── services/              # бизнес-логика
│   │   └── tool_executor.py
│   ├── models/                # pydantic модели
│   └── utils/                 # helper'ы
├── frontend/
│   ├── index.html
│   ├── app.js
│   ├── styles.css
│   └── assets/
│       └── logo.svg
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
### Короткий срок (1–3 недели)
- Подключение реальных инструментов НТ evi-utils
- Рефакторинг структуры проекта
- Поддержка SSH-запуска на удалённых серверах
- История запусков
- Генерация отчетов
- Стабилизация
### Средний срок (1–2 месяца)
- Переезд на модульную структуру (`routers/`, `services/`)
- Создание `config.py` + `.env`
- Логирование + просмотр логов в веб
- Управление пользователями и ролями
- Docker + docker-compose 
- Вывод результатов в реальном времени (SSE)
### Долгосрочные планы
- Подключение evi-tools для EVI-SCUD
- Подключение автотестов + smoke тестирования API
- Celery + Redis для очередей
- Агенты на целевых серверах
- Сравнительная аналитика тестов
- Интеграция с Grafana 

### Git Integration
git remote add origin https://github.com/1velialer-cell/loadstand_dev.git
git branch -M main
git push -u origin main