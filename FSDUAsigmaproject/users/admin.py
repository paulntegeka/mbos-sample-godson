from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


from django.contrib.auth.admin import UserAdmin

UserAdmin.fieldsets += ('FSDU specific field', {'fields': ('phone_number',)}),

class CustomUserAdmin(UserAdmin):
    list_display = ['username','email',  'phone_number', 'is_staff', ]
    
admin.site.register(CustomUser,CustomUserAdmin)