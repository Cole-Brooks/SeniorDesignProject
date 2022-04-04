from django.contrib import admin
from .models import Car, ParkingHistory


# Register your models here.
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'make', 'model', 'license_plate_number', 'in_time', 'out_time')


# Register ParkingHistory model.
@admin.register(ParkingHistory)
class ParkingHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'parking', 'in_time', 'out_time', 'parking_fee',)

    actions = None
