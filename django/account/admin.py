from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('screen_name', 'twitter_id', 'is_staff')
    fields = ('screen_name', 'twitter_id', 'is_protected', 'is_staff', 'is_superuser')
    ordering = ('screen_name', )
admin.site.register(User, CustomUserAdmin)
