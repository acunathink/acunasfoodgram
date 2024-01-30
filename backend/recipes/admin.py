from django.contrib import admin

from recipes.models import Ingredient, Recipe, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    list_editable = list_display


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    list_editable = list_display


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'text',
        'cooking_time'
        'author',
        'ingredients',
        'tags',
    )
    list_editable = list_display
    list_select_related = True


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
