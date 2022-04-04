# Generated by Django 4.0.1 on 2022-04-04 19:25

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administrators', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=255)),
                ('license_plate_number', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('in_time', models.TimeField(null=True)),
                ('out_time', models.TimeField(null=True)),
            ],
            options={
                'verbose_name': 'Car',
                'verbose_name_plural': 'Cars',
            },
        ),
        migrations.CreateModel(
            name='ParkingHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_time', models.TimeField(null=True)),
                ('out_time', models.TimeField(null=True)),
                ('parking_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('paid', models.BooleanField(default=False)),
                ('payment_date', models.DateField(null=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.car')),
                ('parking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrators.parkinglot')),
            ],
            options={
                'verbose_name': 'parking-history',
                'verbose_name_plural': 'parking-histories',
            },
        ),
    ]
