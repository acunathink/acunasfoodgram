# praktikum_new_diplom

## Описание
Проект «Фудграм» — сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также доступен сервис «Список покупок». Он позволяет создавать список продуктов, которые нужно купить для приготовления выбранных блюд сохраняя его в формате json, и может использоваться сторонними сервисами или приложениями.


### Как настроить проект для запуска:

- Установите [Docker](https://docs.docker.com/engine/install/)

- Клонируйте репозиторий и перейдите в него в командной строке:
```
git clone git@github.com:acunathink/foodgram-project-react.git

cd foodgram-project-react
```

- Создайте файл `.env` на основе `.env.examlpe`:
  Установите пароль для доступа к базе данных (`POSTGRES_PASSWORD`),
  `DJANGO_SECRET_KEY` измените по своему усмотрению.

  Добавьте в настройки доменное имя или ip-адрес связанные с вашим сервером,
  для этого замените значение `DJANGO_HOST` (опционально),
  или удалите это поле, тогда сайт будет доступен только локально,
  по адресу http://localhost:8000


### Запуск проекта

    В корневой папке проекта (по умолчанию - `foodgram-project-react`) выполните:
```
docker compose -f docker-compose.production.yml up
```
