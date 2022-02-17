from django.contrib import admin
from .models import ParkingLot


# Register your models here.
@admin.register(ParkingLot)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ('id', 'administrator', 'parking_name', 'phone')
