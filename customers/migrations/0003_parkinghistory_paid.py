# Generated by Django 4.0.1 on 2022-04-02 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkinghistory',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
