from django.contrib import admin
from django.db.models import Count

from .models import Ingredient, Recipe, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = 'name', 'measurement_unit'
    search_fields = 'name',
    list_filter = 'measurement_unit',
    list_display_links = 'name',
    list_editable = 'measurement_unit',


class TagAdmin(admin.ModelAdmin):
    list_display = 'name', 'color', 'slug'
    list_display_links = 'name',
    list_editable = 'color',


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'cooking_time', 'favorites_count',
                    'created', 'author')
    search_fields = 'name', 'author__username'
    list_filter = 'tags', 'cooking_time', 'ingredients'
    list_display_links = 'name',

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(fav_count=Count('favored'))

    def favorites_count(self, instance):
        return instance.fav_count


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
