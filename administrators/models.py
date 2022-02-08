from django.db import models
# from users.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from django.conf import settings
from ckeditor.fields import RichTextField
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth.models import User
from users.models import User


# Create your models here.

class ParkingLot(models.Model):
    """This is the Parking user model"""

    administrator = models.ForeignKey(User, on_delete=models.CASCADE)
    parking_name = models.CharField(blank=False, null=False, max_length=255)
    full_address = models.CharField(blank=False, null=False, max_length=255)
    phone = PhoneNumberField()

    class Meta:
        verbose_name = 'Parking Lot'
        verbose_name_plural = 'Parking Lots'

    def __str__(self):
        return self.administrator.first_name + self.administrator.last_name
