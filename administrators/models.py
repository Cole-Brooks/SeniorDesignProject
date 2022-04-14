from decimal import Decimal
from django.core.validators import MinValueValidator
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
from django.utils.translation import gettext as _
# from customers.models import Car
from users.models import User
from localflavor.us.models import USStateField, USZipCodeField


# Create your models here.

class ParkingLot(models.Model):
    """This is the Parking user model"""

    administrator = models.ForeignKey(User, related_name='parking_added', on_delete=models.CASCADE)
    parking_name = models.CharField(blank=False, null=False, max_length=255)
    overview = RichTextField(blank=True, null=True)
    street_address = models.CharField(blank=False, null=False, max_length=255)
    city = models.CharField(blank=False, null=False, max_length=255)
    state = USStateField(null=False, blank=False)
    zip_code = models.CharField(_("zip code"), max_length=5, default="52246")
    phone = PhoneNumberField(null=False, blank=False, unique=False)
    business_email = models.EmailField(blank=False, null=False, max_length=255)
    added_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True)
    customer = models.ManyToManyField(User, related_name='customers_who_joined', blank=True)
    capacities = models.PositiveIntegerField(blank=False, null=False)
    image = models.ImageField(blank=True, null=True, upload_to="parking_lots")
    fee_per_hour = models.DecimalField(max_digits=8, decimal_places=2, default=1.0,
                                       validators=[MinValueValidator(Decimal('0.00'))])
    free_spots = models.PositiveIntegerField(blank=False, null=False, validators=[MinValueValidator(0)])
    max_overdue = models.DecimalField(max_digits=8, decimal_places=2, default=0.0,
                                      validators=[MinValueValidator(Decimal('0.00'))])

    class Meta:
        verbose_name = 'Parking Lot'
        verbose_name_plural = 'Parking Lots'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.parking_name)
        super(ParkingLot, self).save(*args, **kwargs)

    def __str__(self):
        return self.parking_name

    @property
    def parking_full_address(self):
        return self.street_address + ", " + self.city + ", " + self.state + " " + self.zip_code

    @property
    def get_business_email(self):
        return self.business_email

    @property
    def get_parking_name(self):
        return self.parking_name

    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "https://res.cloudinary.com/dh13i9dce/image/upload/v1642216377/media/avatars/defaultprofile_vad1ub.png"

