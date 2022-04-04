# Generated by Django 4.0.1 on 2022-04-04 19:25

import ckeditor.fields
from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import localflavor.us.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParkingLot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parking_name', models.CharField(max_length=255)),
                ('overview', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('street_address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', localflavor.us.models.USStateField(max_length=2)),
                ('zip_code', models.CharField(default='52246', max_length=5, verbose_name='zip code')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('business_email', models.EmailField(max_length=255)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('capacities', models.PositiveIntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='parking_lots')),
                ('fee_per_hour', models.DecimalField(decimal_places=2, default=1.0, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('free_spots', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('max_overdue', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
            ],
            options={
                'verbose_name': 'Parking Lot',
                'verbose_name_plural': 'Parking Lots',
            },
        ),
    ]
