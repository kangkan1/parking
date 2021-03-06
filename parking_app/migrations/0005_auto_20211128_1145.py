# Generated by Django 3.2.9 on 2021-11-28 11:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('parking_app', '0004_rename_userprofile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=150, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('ranged', models.DecimalField(decimal_places=1, max_digits=2)),
                ('vehicle', models.CharField(choices=[('T', 'Two Wheeler'), ('F', 'Four Wheeler'), ('S', 'SUV')], max_length=1)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
