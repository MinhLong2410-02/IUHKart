# Generated by Django 5.1.3 on 2024-11-24 13:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('discount_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('discount_percent', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'db_table': 'discounts',
            },
        ),
        migrations.CreateModel(
            name='OrderProductDiscount',
            fields=[
                ('product_discount_id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('discount', models.ForeignKey(db_column='discount_id', on_delete=django.db.models.deletion.CASCADE, to='discount.discount')),
                ('product', models.ForeignKey(db_column='product_id', on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'db_table': 'order_product_discounts',
                'indexes': [models.Index(fields=['start_date'], name='order_produ_start_d_5c9ea9_idx'), models.Index(fields=['end_date'], name='order_produ_end_dat_879853_idx')],
            },
        ),
    ]
