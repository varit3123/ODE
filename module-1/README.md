# Водить.РФ - модуль 1

Отдельный Django-проект для первой части экзамена. Визуал здесь специально простой: основной дизайн делается во втором модуле.

## Запуск

```bash
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py seed_demo
py manage.py runserver 127.0.0.1:8001
```

Открыть: `http://127.0.0.1:8001/module-1/`

Можно выбрать любой свободный порт:

```bash
py manage.py runserver 127.0.0.1:8081
```

## Доступы

- Пользователь: `demo26` / `Demo2026`
- Администратор задания: `Admin26` / `Demo20`
