from django.contrib import admin
from .models import ParkingLot


# Register your models here.
@admin.register(ParkingLot)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ('id', 'administrator', 'parking_name', 'phone')

    actions = None

    def save_model(self, request, obj, form, change):
        if not obj.administrator:
            obj.administrator = request.user
        obj.save()
