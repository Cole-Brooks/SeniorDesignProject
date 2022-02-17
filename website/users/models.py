from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from django.conf import settings
from ckeditor.fields import RichTextField
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


# Create your models here.

class User(AbstractUser):
    """This is the administrator user model"""
    #parking_administrator = models.BooleanField(default=False)
    USER_TYPES = (
        [('Parking Administrator', 'Parking Administrator'),
        ('Customer', 'Customer'),])
    Please_check_this_if_you_are_a_parking_administrator = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.first_name + " " + self.last_name



