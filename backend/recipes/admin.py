from django.contrib import admin

from recipes.models import Ingredient, Tag


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


admin.site.register(Tag)
admin.site.register(Ingredient)
