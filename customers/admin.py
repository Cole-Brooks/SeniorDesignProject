from django.contrib import admin
from .models import Car, ParkingHistory, DuePaymentReminder


# Register your models here.
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'make', 'model', 'license_plate_number', 'in_time', 'out_time')


# Register ParkingHistory model.
@admin.register(ParkingHistory)
class ParkingHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'parking', 'in_time', 'out_time', 'parking_fee', 'payment_date')

    actions = None


# Register DuePaymentReminder model.
@admin.register(DuePaymentReminder)
class DuePaymentReminderAdmin(admin.ModelAdmin):
    list_display = ('id', 'parking', 'amount_due', 'email_to', 'has_been_sent')

    actions = None
