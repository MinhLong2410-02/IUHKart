# Generated by Django 5.1.3 on 2024-11-13 09:13

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_initial'),
        ('order', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('discount_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('discount_percent', models.DecimalField(decimal_places=2, max_digits=5)),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('in_use', models.BooleanField(default=True)),
                ('product', models.ForeignKey(db_column='product_id', on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('vendor', models.ForeignKey(db_column='vendor_id', on_delete=django.db.models.deletion.CASCADE, to='account.vendor')),
            ],
            options={
                'db_table': 'discounts',
            },
        ),
        migrations.CreateModel(
            name='OrderProductDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discount.discount')),
                ('order_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.orderproduct')),
            ],
            options={
                'db_table': 'order_product_discounts',
            },
        ),
        migrations.AddIndex(
            model_name='discount',
            index=models.Index(fields=['start_date'], name='discounts_start_d_3369b2_idx'),
        ),
        migrations.AddIndex(
            model_name='discount',
            index=models.Index(fields=['end_date'], name='discounts_end_dat_53459a_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='orderproductdiscount',
            unique_together={('order_product', 'discount')},
        ),
    ]
