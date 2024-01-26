from django.contrib import admin

from recipes.models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    list_editable = list_display


admin.site.register(Tag)
