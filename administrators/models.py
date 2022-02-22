from django.db import models
# from users.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from django.conf import settings
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth.models import User
from users.models import User


# Create your models here.

class ParkingLot(models.Model):
    """This is the Parking user model"""

    administrator = models.ForeignKey(User, related_name='parking_added', on_delete=models.CASCADE)
    parking_name = models.CharField(blank=False, null=False, max_length=255)
    overview = RichTextField(blank=True, null=True)
    street_address = models.CharField(blank=False, null=False, max_length=255)
    city = models.CharField(blank=False, null=False, max_length=255)
    state = models.CharField(blank=False, null=False, max_length=255)
    zip_code = models.CharField(blank=False, null=False, max_length=255)
    phone = PhoneNumberField(null=False, blank=False, unique=False)
    added_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True)
    customer = models.ManyToManyField(User, related_name='parking_joined', blank=True)
    capacities = models.PositiveIntegerField(blank=False, null=False)

    class Meta:
        verbose_name = 'Parking Lot'
        verbose_name_plural = 'Parking Lots'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.parking_name)
        super(ParkingLot, self).save(*args, **kwargs)

    def __str__(self):
        return self.administrator.first_name + self.administrator.last_name

    def parking_full_address(self):
        return self.street_address + ", " + self.city + ", " + self.state + ", " + self.zip_code
