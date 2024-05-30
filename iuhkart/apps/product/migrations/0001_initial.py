# Generated by Django 5.0.2 on 2024-05-30 06:33

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
                'db_table': 'category',
                'ordering': ['-category_id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=255)),
                ('original_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.PositiveIntegerField()),
                ('brand', models.CharField(max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, max_length=255, populate_from='product_name')),
                ('product_description', models.TextField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_add', models.DateField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category')),
                ('created_by', models.ForeignKey(db_column='vendor_id', on_delete=django.db.models.deletion.CASCADE, to='account.vendor')),
            ],
            options={
                'verbose_name_plural': 'Products',
                'db_table': 'product',
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
