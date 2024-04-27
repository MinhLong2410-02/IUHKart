from iuhkart.wsgi import *
from django.contrib.auth import get_user_model
from apps.product.models import Category, Product, CategoryProduct
from apps.vendor.models import Vendor
from apps.customers.models import Customer, User
from apps.address.models import Province, District, Ward
import pandas as pd
from django.contrib.auth.hashers import make_password
import json
import os
os.system('migrate.bat')

def insert_address():
    province_df = pd.read_csv('https://raw.githubusercontent.com/MinhLong2410-02/VN-province-api-test/main/province.csv')
    district_df = pd.read_csv('https://raw.githubusercontent.com/MinhLong2410-02/VN-province-api-test/main/district.csv')
    ward_df = pd.read_csv('https://raw.githubusercontent.com/MinhLong2410-02/VN-province-api-test/main/ward.csv')
    provinces = province_df.to_dict('records')
    districts = district_df.to_dict('records')
    wards = ward_df.to_dict('records')
    province_objs = [Province(
        province_id=int(province['province_id']),
        province_name=province['province_name'],
        province_name_en=province['province_name_en'],
        type=province['type']
    ) for province in provinces]
    Province.objects.bulk_create(province_objs)
    province_cache = {p.province_id: p for p in Province.objects.all()}
    district_objs = [District(
        district_id=int(district['district_id']),
        province_id=province_cache[int(district['province_id'])],
        district_name=district['district_name'],
        district_name_en=district['district_name_en'],
        type=district['type']
    ) for district in districts]
    District.objects.bulk_create(district_objs)
    district_cache = {d.district_id: d for d in District.objects.all()}
    ward_objs = [Ward(
        ward_id=int(ward['ward_id']),
        district_id=district_cache[int(ward['district_id'])],
        province_id=province_cache[int(ward['province_id'])],
        ward_name=ward['ward_name'],
        ward_name_en=ward['ward_name_en'],
        type=ward['type']
    ) for ward in wards]
    Ward.objects.bulk_create(ward_objs)

def insert_category():
    category_df = pd.read_csv('https://raw.githubusercontent.com/MinhLong2410-02/IUHKart/main/schema/Database/categories.csv?token=GHSAT0AAAAAACNO47DOPCF3BEIKDNAK5KSUZRMTRGA')
    categories = category_df.to_dict('records')
    category_objs = [Category(
        category_id = category['category_id'],
        slug = category['slug'],
        category_name=category['name'],
        category_img_url=category['category_img_url']
    ) for category in categories]
    Category.objects.bulk_create(category_objs)
    category_cache = {c.category_id: c for c in Category.objects.all()}
    return category_cache

insert_address()
insert_category()
user1 = User.objects.create_user(
        email='minhlong2002@gmail.com',
        password=make_password('123'),
        is_vendor=True,
    )
vendor1 = Vendor.objects.create(
        user=user1,
        name='Minh Long',
        phone='1234567890',
        description='This is a description for Vendor One.'
    )
user2 = User.objects.create_user(
    email='vanhau20022018@gmail.com',
    password=make_password('123'),
    is_vendor=True,
)
vendor2 = Vendor.objects.create(
    user=user2,
    name='Văn Hậu',
    phone='1234567891',
    description='This is a description for Vendor Two.'
)
user3 = User.objects.create_user(
    email='quachnam311@gmail.com',
    password=make_password('123'),
    is_vendor=True,
)
vendor3 = Vendor.objects.create(
    user=user3,
    name='Qx Nam',
    phone='1234567892',
    description='This is a description for Vendor Three.'
)
