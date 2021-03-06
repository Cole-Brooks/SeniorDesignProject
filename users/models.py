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

    Please_check_this_if_you_are_a_parking_administrator = models.BooleanField(default=False)
    balance_due = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.first_name + " " + self.last_name

    def get_full_name(self):
        return self.first_name + " " + self.last_name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'

    @property
    def get_avatar_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return "https://res.cloudinary.com/dh13i9dce/image/upload/v1642216377/media/avatars/defaultprofile_vad1ub.png"


class Contact(models.Model):
    """Model for user contact"""
    name = models.CharField(verbose_name="Name", max_length=250)
    email = models.CharField(verbose_name="Email", max_length=250)
    message = models.TextField(verbose_name="Message")
    phone = models.CharField(verbose_name="Phone number", max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return self.name + " " + self.email
