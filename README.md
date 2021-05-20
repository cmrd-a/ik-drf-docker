# ik-drf-docker

Гостевая книга: записи, лайки, OAuth-авторизация, юнит-тесты.

Каждую минуту удаляются записи с запрещёнными словами.

* Django REST framework
* Celery-beat
* Simple JWT
* Docker compose

## Запуск:

`cp .env.example .env`

`docker compose up -d`

## Тесты:

`docker compose run app python manage.py test`

## Остановка:

`docker compose down`

Swagger: http://localhost:8000/swagger

Админка: http://localhost:8000/admin