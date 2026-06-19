# Водить.РФ - общая папка проекта

Основная папка проекта называется `Общая для всех`.

Структура:

- `module-1` - первая часть работы, базовый Django-проект.
- `module-2` - вторая часть работы, доработанный Django-проект.
- `databases` - SQLite-базы двух модулей.
- `docs` - схемы базы данных и ER-диаграммы.

Папка `materials` не используется и игнорируется через `.gitignore`.

## Запуск модуля 1

```powershell
cd "C:\Users\zhail\Desktop\Общая для всех\module-1"
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py seed_demo
py manage.py runserver 127.0.0.1:8001
```

Открыть: `http://127.0.0.1:8001/module-1/`

## Запуск модуля 2

```powershell
cd "C:\Users\zhail\Desktop\Общая для всех\module-2"
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py seed_demo
py manage.py runserver 127.0.0.1:8000
```

Открыть: `http://127.0.0.1:8000/module-2/`

## Доступы

- Администратор: `Admin26` / `Demo20`
- Пользователь: `demo26` / `Demo2026`
- Второй пользователь: `anna26` / `River2026`
