from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тэг',
        max_length=144,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=16,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True
    )

    def __str__(self) -> str:
        return self.slug

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'Тэги'


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Ингредиент',
        max_length=144,
        unique=True
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=64,
        unique=False
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=144,
        unique=True,
        null=False,
        blank=False
    )
    text = models.CharField(
        verbose_name='Описание',
        max_length=4096,
        null=False,
        blank=False
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления в минутах',
        default=0,
        null=False,
        blank=False
    )
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to='images/',
        null=False,
        blank=False
    )
    author = models.ForeignKey(
        User, related_name='ricipes',
        on_delete=models.CASCADE
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredients',
        blank=False
    )
    tags = models.ManyToManyField(
        Tag, through='RecipeTags',
        blank=False
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-created', )


class RecipeIngredients(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='recipes')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE)
    amount = models.SmallIntegerField(
        null=False,
    )

    def __str__(self):
        return f'{self.recipe} {self.ingredient} {self.amount}'


class RecipeTags(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipe} {self.tag}'


class Subscriber(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscribe')
    subscribe = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscription')

    class Meta:
        ordering = ('author', )
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'subscribe'],
                name='once_subscribe'
            )
        ]
