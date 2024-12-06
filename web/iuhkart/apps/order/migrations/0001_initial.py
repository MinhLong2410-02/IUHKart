# Generated by Django 5.1.3 on 2024-12-06 07:18

import apps.order.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('address', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_number', models.CharField(db_index=True, max_length=50, unique=True)),
                ('shipping_date', models.DateTimeField(default=apps.order.models.default_shipping_date)),
                ('order_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('order_status', models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], db_index=True, default='pending', max_length=50)),
                ('order_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('address', models.ForeignKey(blank=True, db_column='address_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='address.address')),
                ('customer', models.ForeignKey(db_column='customer_id', on_delete=django.db.models.deletion.CASCADE, to='account.customer')),
            ],
            options={
                'db_table': 'orders',
                'ordering': ['-order_date'],
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('order_product_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('order', models.ForeignKey(db_column='order_id', on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('product', models.ForeignKey(db_column='product_id', on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'db_table': 'order_products',
                'ordering': ['-order_id'],
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('transation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_money', models.DecimalField(decimal_places=2, max_digits=12)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed'), ('refunded', 'Refunded')], default='pending', max_length=50)),
                ('customer', models.ForeignKey(db_column='customer_id', on_delete=django.db.models.deletion.CASCADE, to='account.customer')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='order.order')),
            ],
            options={
                'db_table': 'transactions',
                'ordering': ['-transation_date'],
            },
        ),
    ]
