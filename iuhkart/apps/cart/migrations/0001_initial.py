# Generated by Django 5.0.2 on 2024-05-25 19:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart_id', models.AutoField(primary_key=True, serialize=False)),
                ('grand_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('items_total', models.PositiveIntegerField()),
                ('customer_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.customer')),
            ],
            options={
                'verbose_name_plural': 'Carts',
                'db_table': 'cart',
                'ordering': ['-cart_id'],
            },
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('cart_product_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField()),
                ('cart_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.cart')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='product_id',
            field=models.ManyToManyField(through='cart.CartProduct', to='product.product'),
        ),
    ]
