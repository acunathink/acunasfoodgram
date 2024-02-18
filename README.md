# [praktikum_new_diplom](https://acunasfoodgram.hopto.org)


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

- В корневой папке проекта (по умолчанию - `foodgram-project-react`) выполните:
```
docker compose up
```
- при отсутствии ошибок можно остановить работу через ^C и запустить в фоновом режиме,
  используя флаг -d:
```
docker compose up -d
```

- после чего можно создать суперюзера для доступа к адимин-зоне сайта, выполнив
```
docker compose exec -it backend python manage.py createsuperuser
```
проверьте, пройдя на  http://localhost:8000/admin/
