from iuhkart.wsgi import *
from django.contrib.auth import get_user_model
from apps.product.models import Category, Product
from apps.account.models import Vendor, Customer, User
from apps.address.models import Province, District, Ward
import pandas as pd
from django.contrib.auth.hashers import make_password
import json, random
import os
from rest_framework_simplejwt.tokens import RefreshToken

os.system('migrate.bat')

import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

path = {
    'province': 'https://raw.githubusercontent.com/MinhLong2410-02/VN-province-api-test/main/province.csv',
    'district': 'https://raw.githubusercontent.com/MinhLong2410-02/VN-province-api-test/main/district.csv',
    'ward': 'https://raw.githubusercontent.com/MinhLong2410-02/VN-province-api-test/main/ward.csv',
    'category': '../schema/Database/categories.csv',
    'product': '../schema/Database/products.csv',
}

########################
# Address
########################
def insert_address():
    try:
        province_df = pd.read_csv(path['province'])
        district_df = pd.read_csv(path['district'])
        ward_df = pd.read_csv(path['ward'])
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
        print(f'✅ {Province.__name__}')
    except Exception as e:
        print(f'❌ {Province.__name__} - {e}')

    try:
        province_cache = {p.province_id: p for p in Province.objects.all()}
        district_objs = [District(
            district_id=int(district['district_id']),
            province_id=province_cache[int(district['province_id'])],
            district_name=district['district_name'],
            district_name_en=district['district_name_en'],
            type=district['type']
        ) for district in districts]
        District.objects.bulk_create(district_objs)
        print(f'✅ {District.__name__}')
    except Exception as e:
        print(f'❌ {District.__name__} - {e}')

    try:
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
        print(f'✅ {Ward.__name__}')
    except Exception as e:
        print(f'❌ {Ward.__name__} - {e}')

########################
# Category 
########################
def insert_category():
    try:
        category_df = pd.read_csv(path['category'])
        categories = category_df.to_dict('records')
        category_objs = [Category(
            category_id = category['category_id'],
            slug = category['slug'],
            category_name=category['name'],
            category_img_url=category['category_img_url']
        ) for category in categories]
        Category.objects.bulk_create(category_objs)
        print(f'✅ {Category.__name__}')
    except Exception as e:
        print(f'❌ {Category.__name__} - {e}')

########################
# Product
########################
def insert_product():
    try:
        df = pd.read_csv(path['product'])
        # process
        vendor_id_list = [1, 2, 3]
        df['vendor_id'] = df['vendor_id'].apply(lambda _: random.choice(vendor_id_list))
        df = df.drop_duplicates('product_id')

        # convert to dict
        df = df.to_dict('records')
        vendor_cache = {x.id: x for x in Vendor.objects.all()}
        category_cache = {x.category_id: x for x in Category.objects.all()}

        model_objs = [Product(
            product_id=rc['product_id'],
            product_name=rc['product_name'],
            original_price=rc['original_price'],
            stock=rc['stock'],
            brand=rc['brand'],
            created_by=vendor_cache[rc['vendor_id']],
            category=category_cache[rc['category_id']]
        ) for rc in df]
        Product.objects.bulk_create(model_objs)
        print(f'✅ {Product.__name__}')
    except Exception as e:
        print(f'❌ {Product.__name__} - {e}')

########################
# user - vendor
########################
def create_user_with_jwt(email, password, is_vendor, name, phone, description):
    user = User.objects.create_user(
        email=email,
        password=password,  # No need to hash the password here
        is_vendor=is_vendor,
    )
    vendor = Vendor.objects.create(
        user=user,
        name=name,
        phone=phone,
        description=description
    )
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    return user, vendor, access_token, refresh_token

user1, vendor1, token1, refresh1 = create_user_with_jwt(
    email='minhlong2002@gmail.com',
    password='123',  # Pass the plain password
    is_vendor=True,
    name='Minh Long',
    phone='1234567890',
    description='This is a description for Vendor One.'
)
print(f'User: {user1.email}, Access Token: {token1}, Refresh Token: {refresh1}')

user2, vendor2, token2, refresh2 = create_user_with_jwt(
    email='vanhau20022018@gmail.com',
    password='123',  # Pass the plain password
    is_vendor=True,
    name='Văn Hậu',
    phone='1234567891',
    description='This is a description for Vendor Two.'
)
print(f'User: {user2.email}, Access Token: {token2}, Refresh Token: {refresh2}')

user3, vendor3, token3, refresh3 = create_user_with_jwt(
    email='quachnam311@gmail.com',
    password='123',  # Pass the plain password
    is_vendor=True,
    name='Qx Nam',
    phone='0398089311',
    description='This is a description for Vendor Three.'
)
print(f'User: {user3.email}, Access Token: {token3}, Refresh Token: {refresh3}')

insert_address()
insert_category()
insert_product()
