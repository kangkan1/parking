# Generated by Django 3.2.9 on 2021-11-30 09:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_app', '0006_registration_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
