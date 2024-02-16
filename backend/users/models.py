from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField('Имя', max_length=144, blank=False)
    last_name = models.CharField('Фамилия', max_length=144, blank=False)
    email = models.EmailField(
        'Адрес почты', max_length=144, blank=False, unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('first_name', 'last_name', 'username')
