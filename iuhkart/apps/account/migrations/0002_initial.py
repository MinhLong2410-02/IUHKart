# Generated by Django 5.0.2 on 2024-09-29 14:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='cart',
            field=models.OneToOneField(blank=True, db_column='cart_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.cart'),
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userrole',
            name='roles',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.role'),
        ),
        migrations.AddField(
            model_name='userrole',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(related_name='users', through='account.UserRole', to='account.role'),
        ),
        migrations.AddField(
            model_name='vendor',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='vendor',
            field=models.OneToOneField(db_column='vendor_id', on_delete=django.db.models.deletion.CASCADE, related_name='bank_account', to='account.vendor'),
        ),
        migrations.AlterUniqueTogether(
            name='userrole',
            unique_together={('user', 'roles')},
        ),
    ]
