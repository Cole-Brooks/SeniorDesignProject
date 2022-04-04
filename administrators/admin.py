from django.contrib import admin
from .models import ParkingLot


# Register ParkingLot model.
@admin.register(ParkingLot)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ('id', 'administrator', 'parking_name', 'phone', 'fee_per_hour', 'max_overdue',)

    actions = None

    def save_model(self, request, obj, form, change):
        if not obj.administrator:
            obj.administrator = request.user
        obj.save()




