# Водить.РФ - модуль 2

Отдельный Django-проект для второй части экзамена. Это версия с дизайном, слайдером, фильтрами, сортировкой и пагинацией.

## Запуск

```bash
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py seed_demo
py manage.py runserver 127.0.0.1:8000
```

Открыть: `http://127.0.0.1:8000/module-2/`

Можно выбрать любой свободный порт:

```bash
py manage.py runserver 127.0.0.1:8080
```

## Доступы

- Пользователь: `demo26` / `Demo2026`
- Дополнительный пользователь: `anna26` / `River2026`
- Администратор задания: `Admin26` / `Demo20`
