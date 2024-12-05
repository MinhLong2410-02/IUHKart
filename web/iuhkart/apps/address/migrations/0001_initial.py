# Generated by Django 5.1.3 on 2024-11-27 17:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Province',
            fields=[
                ('province_id', models.AutoField(primary_key=True, serialize=False)),
                ('province_name', models.CharField(max_length=50)),
                ('province_name_en', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Provinces',
                'db_table': 'provinces',
                'ordering': ['province_name'],
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('district_id', models.AutoField(primary_key=True, serialize=False)),
                ('district_name', models.CharField(max_length=50)),
                ('district_name_en', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=30)),
                ('province_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.province')),
            ],
            options={
                'verbose_name_plural': 'Districts',
                'db_table': 'districts',
                'ordering': ['district_name'],
            },
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('ward_id', models.AutoField(primary_key=True, serialize=False)),
                ('ward_name', models.CharField(max_length=50)),
                ('ward_name_en', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=30)),
                ('district_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.district')),
                ('province_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.province')),
            ],
            options={
                'verbose_name_plural': 'Wards',
                'db_table': 'wards',
                'ordering': ['ward_name'],
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('address_id', models.AutoField(primary_key=True, serialize=False)),
                ('address_detail', models.CharField(blank=True, max_length=200, null=True)),
                ('district_id', models.ForeignKey(blank=True, db_column='district_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='address.district')),
                ('province_id', models.ForeignKey(blank=True, db_column='province_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='address.province')),
                ('ward_id', models.ForeignKey(blank=True, db_column='ward_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='address.ward')),
            ],
            options={
                'db_table': 'addresses',
            },
        ),
    ]
