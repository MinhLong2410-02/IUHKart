from django.db import models

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    province_id = models.ForeignKey('Province', models.DO_NOTHING, db_column='province_id', blank=True, null=True, unique=False)
    district_id = models.ForeignKey('District', models.DO_NOTHING, db_column='district_id', blank=True, null=True)
    ward_id = models.ForeignKey('Ward', models.DO_NOTHING, db_column='ward_id', blank=True, null=True)
    
    address_detail = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'addresses'

class Province(models.Model):
    province_id = models.AutoField(primary_key=True)
    province_name = models.CharField(max_length=50)
    province_name_en = models.CharField(max_length=50)
    type = models.CharField(max_length=30)
    class Meta:
        db_table = 'provinces'
        verbose_name_plural = 'Provinces'
        ordering = ['province_name']

class District(models.Model):
    district_id = models.AutoField(primary_key=True)
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE)
    district_name = models.CharField(max_length=50)
    district_name_en = models.CharField(max_length=50)
    type = models.CharField(max_length=30)
    class Meta:
        db_table = 'districts'
        verbose_name_plural = 'Districts'
        ordering = ['district_name']

class Ward(models.Model):
    ward_id = models.AutoField(primary_key=True)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE)
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE)
    ward_name = models.CharField(max_length=50)
    ward_name_en = models.CharField(max_length=50)
    type = models.CharField(max_length=30)
    class Meta:
        db_table = 'wards'
        verbose_name_plural = 'Wards'
        ordering = ['ward_name']