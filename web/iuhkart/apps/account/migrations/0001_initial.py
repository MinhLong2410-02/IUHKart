# Generated by Django 5.1.3 on 2024-11-13 13:45

import apps.account.manager
import apps.custom_storage
import django.contrib.postgres.fields
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('bank_account_id', models.AutoField(db_column='bank_account_id', primary_key=True, serialize=False)),
                ('bank_name', models.CharField(max_length=255, null=True)),
                ('account_number', models.CharField(max_length=255, null=True)),
                ('account_holder_name', models.CharField(max_length=255, null=True)),
                ('branch_name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'bank_accounts',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=17, null=True)),
                ('fullname', models.CharField(max_length=255)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('age', models.SmallIntegerField()),
                ('avatar_url', models.ImageField(blank=True, max_length=255, null=True, storage=apps.custom_storage.AzureCustomerStorage(), upload_to='')),
                ('date_join', models.DateField(default=django.utils.timezone.now)),
                ('recommend_products', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, db_column='recommend_product_ids', default=list, size=20)),
            ],
            options={
                'verbose_name_plural': 'Customers',
                'db_table': 'customers',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('logo_url', models.ImageField(blank=True, null=True, storage=apps.custom_storage.AzureVendorStorage(), upload_to='')),
                ('date_join', models.DateField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'Vendors',
                'db_table': 'vendors',
            },
        ),
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
                'db_table': 'users',
            },
            managers=[
                ('objects', apps.account.manager.UserManager()),
            ],
        ),
    ]
