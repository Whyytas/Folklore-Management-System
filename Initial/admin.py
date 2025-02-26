from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username',  'role')  # Add fields to display
    fieldsets = UserAdmin.fieldsets + (  # Add custom fields in the admin form
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (  # Include custom fields when adding a user
        (None, {'fields': ('role',)}),
    )