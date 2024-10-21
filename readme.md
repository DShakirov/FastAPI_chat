Тестовое задание
    Цель: 
        Разработать приложение для регистрации пользователей и их общения в чате. 
        Пользователям оффлайн отправляется сообщение в телеграм.
        Реализовать простейший фронтенд для теста приложения.
    Стек: FastAPI, Celery, postgreSQL, redis, docker, pytest, aiogram, nginx.
    Инструкция по запуску:
        - склонировать репозиторий.
        - заполнить .env.docker и опционально .env.tests по образцу из env.example
        - запустить контейнеры командой ```docker-compose up --build```
        - опционально: запустить автотесты можно собрав docker-compose.tests.yaml
        - по адресу "pages/" доступны шаблоны для авторизации, регистрации и чата(для чата требуется регистрация)
    