from django.contrib import admin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from .models import User


class UserAdmin(ModelAdmin):
	list_display = ['username','first_name' , 'last_name',  'is_superuser','is_active','email']
	ordering = ['username']
	list_filter=('is_superuser','is_active')

admin.site.register(User,UserAdmin)

admin.site.unregister(Group)