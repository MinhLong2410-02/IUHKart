# Generated by Django 5.0.2 on 2024-04-28 01:31

import apps.customers.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('is_customer', models.BooleanField(default=False)),
                ('is_vendor', models.BooleanField(default=False)),
                ('address', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='address.address')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'user',
            },
            managers=[
                ('objects', apps.customers.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=255)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('age', models.SmallIntegerField()),
                ('avatar_url', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Customers',
                'db_table': 'customer',
            },
        ),
    ]
