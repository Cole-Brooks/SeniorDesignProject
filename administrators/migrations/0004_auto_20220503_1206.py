# Generated by Django 3.2.13 on 2022-05-03 17:06

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrators', '0003_alter_parkinglot_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parkinglot',
            old_name='phone',
            new_name='phone_number',
        ),
        migrations.AlterField(
            model_name='parkinglot',
            name='fee_per_hour',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
        migrations.AlterField(
            model_name='parkinglot',
            name='max_overdue',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
    ]
