# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role & School', {'fields': ('role', 'school')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role & School', {'fields': ('role', 'school')}),
    )
    list_display = ('username', 'email', 'role', 'school', 'is_staff')

admin.site.register(User, CustomUserAdmin)