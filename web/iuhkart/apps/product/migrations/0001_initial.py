# Generated by Django 5.1.3 on 2024-12-07 04:36

import apps.custom_storage
import autoslug.fields
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=50)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, max_length=100, populate_from='category_name')),
                ('category_img_url', models.URLField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'db_table': 'categories',
                'ordering': ['-category_id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(db_column='product_id', primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=255)),
                ('original_price', models.BigIntegerField()),
                ('stock', models.PositiveIntegerField()),
                ('brand', models.CharField(max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, max_length=255, populate_from='product_name')),
                ('product_description', models.TextField()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('ratings', models.FloatField(default=0.0)),
                ('date_add', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category')),
                ('created_by', models.ForeignKey(db_column='vendor_id', on_delete=django.db.models.deletion.CASCADE, to='account.vendor')),
            ],
            options={
                'verbose_name_plural': 'Products',
                'db_table': 'products',
                'ordering': ['-product_id'],
            },
        ),
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('product_image_id', models.AutoField(primary_key=True, serialize=False)),
                ('image_url', models.ImageField(max_length=255, storage=apps.custom_storage.AzureProductStorage(), upload_to='')),
                ('is_main', models.BooleanField(default=False)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.product')),
            ],
            options={
                'verbose_name_plural': 'Product Images',
                'db_table': 'product_images',
                'ordering': ['product_id', '-is_main'],
            },
        ),
    ]
