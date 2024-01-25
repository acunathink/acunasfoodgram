from django.contrib.auth.models import AbstractUser

# from django.db import models


class User(AbstractUser):
    pass

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('first_name', 'last_name', 'username')
