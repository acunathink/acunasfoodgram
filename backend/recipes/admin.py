from django.contrib import admin

from recipes.models import Ingredient, Recipe, Tag


class RecipeAdmin(admin.ModelAdmin):
    # list_display = (
    #     'name',
    #     'text',
    #     'cooking_time',
    #     'author'
    # )
    # list_editable = [list_display,]
    list_select_related = True


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
