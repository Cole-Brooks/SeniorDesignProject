from django.db import models
# from users.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from django.conf import settings
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from users.models import User


# Create your models here.

class Car(models.Model):
    """This is the Car user model"""

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    mark = models.CharField(blank=False, null=False, max_length=255)
    model = models.CharField(blank=False, null=False, max_length=255)
    licence_plate_number = models.CharField(blank=False, null=False, max_length=255)
    State = models.CharField(blank=False, null=False, max_length=255)

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'

    def __str__(self):
        return self.owner.first_name + self.owner.last_name
