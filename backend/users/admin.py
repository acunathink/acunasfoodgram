from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = 'first_name', 'last_name', 'email', 'is_staff'
    list_editable = 'is_staff',
    search_fields = ('email', 'username')
    list_filter = 'first_name', 'email', 'username'
    list_display_links = ('first_name', 'last_name')


admin.site.register(User, UserAdmin)
