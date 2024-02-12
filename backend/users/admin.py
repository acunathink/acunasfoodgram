from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = 'username', 'first_name', 'last_name', 'email', 'is_staff'
    list_editable = 'is_staff',
    search_fields = 'email', 'username'
    list_filter = 'first_name', 'last_name'
    list_display_links = 'username',


admin.site.register(User, UserAdmin)
