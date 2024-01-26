from django.db import models


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тэг',
        max_length=144,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=64,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'Тэги'
