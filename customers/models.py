import administrators
import datetime
import uuid
import pytz
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from django.conf import settings
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from users.models import User
from django.utils import timezone
from localflavor.us.models import USStateField, USZipCodeField


# Create your models here.

class Car(models.Model):
    """This is the Car user model"""

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.CharField(blank=False, null=False, max_length=255)
    model = models.CharField(blank=False, null=False, max_length=255)
    license_plate_number = models.CharField(blank=False, null=False, max_length=255)
    state = USStateField(null=False, blank=False)
    parking = models.ForeignKey(administrators.models.ParkingLot(), blank=True, null=True, on_delete=models.SET_NULL)
    in_time = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    out_time = models.DateTimeField(auto_now_add=False, blank=True, null=True)

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'

    def __str__(self):
        return self.make + ' ' + self.model

    @property
    def get_time_spent(self):
        return str(datetime.timedelta(seconds=(timezone.now() - self.in_time).seconds))


class ParkingHistory(models.Model):
    """This a model for customers parking history"""
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    parking = models.ForeignKey(administrators.models.ParkingLot, on_delete=models.CASCADE)
    in_time = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    out_time = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    parking_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.0,
                                      validators=[MinValueValidator(Decimal('0.00'))])
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'parking-history'
        verbose_name_plural = 'parking-histories'

    def __str__(self):
        return self.car.make + ' ' + self.car.model + ' ' + self.parking.parking_name

    @property
    def get_parking_fee(self):
        return self.parking_fee

    @property
    def get_date(self):
        return self.payment_date

    @property
    def get_business_email(self):
        return self.parking.business_email

    @property
    def get_parking_name(self):
        return self.parking.parking_name

    @property
    def get_time_spent(self):
        return str(datetime.timedelta(seconds=(self.out_time - self.in_time).seconds))


class DuePaymentReminder(models.Model):
    """This a model for customers parking history"""
    parking = models.CharField(blank=False, null=False, max_length=255)
    amount_due = models.DecimalField(max_digits=8, decimal_places=2, default=0.0,
                                     validators=[MinValueValidator(Decimal('0.00'))])
    email_to = models.EmailField(max_length=255, blank=True, null=True)
    has_been_sent = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'due-payment-reminder'
        verbose_name_plural = 'due-payment-reminders'

    @property
    def get_parking_fee(self):
        return self.parking_fee

    @property
    def get_date(self):
        return self.payment_date

    @property
    def get_business_email(self):
        return self.parking.business_email

    @property
    def get_parking_name(self):
        return self.parking.parking_name
