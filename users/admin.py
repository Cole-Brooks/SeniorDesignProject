from django.contrib import admin
from .models import User, Profile, Contact


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'balance_due',)


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    """Register the model with specific fields"""
    list_display = ['user', 'photo']
    
    
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'timestamp')