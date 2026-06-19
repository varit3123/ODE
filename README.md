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
py manage.py migrate
py manage.py seed_demo
py manage.py runserver 127.0.0.1:8001
```

Открыть: `http://127.0.0.1:8001/module-1/`

## Запуск модуля 2

```powershell
cd "C:\Users\zhail\Desktop\Общая для всех\module-2"
py manage.py migrate
py manage.py seed_demo
py manage.py runserver 127.0.0.1:8000
```

Открыть: `http://127.0.0.1:8000/module-2/`

## Доступы

- Администратор: `Admin26` / `Demo20`
- Пользователь: `demo26` / `Demo2026`
- Второй пользователь: `anna26` / `River2026`

Создание локального Git-репозитория

Откройте новый CMD и по очереди выполните команды:

cd путь_к_папке_с_работой
git init
git config user.name "Любое имя"
git config user.email "Любая почта"
git add .
git commit -m "Создание проекта"

Например, имя и почта могут быть любыми:

git config user.name "Test"
git config user.email "test@local"

После выполнения команд в папке будет создан локальный Git-репозиторий, а все файлы проекта сохранятся в первом коммите.
