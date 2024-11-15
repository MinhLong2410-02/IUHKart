# Generated by Django 5.1.3 on 2024-11-13 13:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart_id', models.AutoField(primary_key=True, serialize=False)),
                ('grand_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('items_total', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Carts',
                'db_table': 'carts',
                'ordering': ['-cart_id'],
            },
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('cart_product_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField()),
                ('cart', models.ForeignKey(db_column='cart_id', on_delete=django.db.models.deletion.CASCADE, related_name='cart_products', to='cart.cart')),
                ('product', models.ForeignKey(db_column='product_id', on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'db_table': 'cart_products',
                'ordering': ['-cart_id'],
            },
        ),
    ]
