from django.contrib import admin
from .models import Car


# Register your models here.
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'mark', 'model', 'licence_plate_number')
