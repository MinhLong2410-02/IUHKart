from iuhkart.wsgi import *
from iuhkart.settings import *
from django.contrib.auth import get_user_model
from apps.product.models import Category, Product, ProductImages
from apps.account.models import Vendor, Customer, User
from apps.address.models import Province, District, Ward, Address
from apps.cart.models import Cart

import pandas as pd
from django.contrib.auth.hashers import make_password
import json, random, sqlite3
import os
from rest_framework_simplejwt.tokens import RefreshToken

import ssl
ssl._create_default_https_context = ssl._create_stdlib_context
print(F'✅ STATUS: {PROJECT_STATUS}')
os.system('migrate.bat')
path = {
    'province': 'https://raw.githubusercontent.com/MinhLong2410-02/VN-province-api-test/main/province.csv',
    'district': 'https://raw.githubusercontent.com/MinhLong2410-02/VN-province-api-test/main/district.csv',
    'ward': 'https://raw.githubusercontent.com/MinhLong2410-02/VN-province-api-test/main/ward.csv',
    'category': '../schema/Database/categories.csv',
    'product': '../schema/Database/products.csv',
    'product_image': '../schema/Database/product_images.csv',
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
        vendor_id_list = [1, 2]
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
        print(e)
        print(f'❌ {Product.__name__} - {e}')

def insert_product_image():
    try:
        df = pd.read_csv(path['product_image'])

        # process
        df.drop_duplicates(subset=['product_img_id', 'product_id'], inplace=True)
        df_ = df['product_id'].value_counts().to_frame().reset_index()
        limit5 = df_[df_['count']<=5]['product_id'].values
        unlimit5 = df_[df_['count']>5]['product_id'].values
        df['is_main'] = df['product_id'].apply(lambda x: True if x in limit5 else False)
        for _id in unlimit5:
            product_img_id_5 = df[df['product_id']==_id].sample(5)['product_img_id'].values
            df['is_main'] = df['product_img_id'].apply(lambda x: True if x in product_img_id_5 else False)
        del df_, limit5, unlimit5
        df.columns = ['product_image_id', 'product_id', 'image_url', 'is_main']

        # convert to dict
        df = df.to_dict('records')
        product_cache = {x.product_id: x for x in Product.objects.all()}

        model_objs = [ProductImages(
            product_image_id=rc['product_image_id'],
            product_id=product_cache[rc['product_id']],
            image_url=rc['image_url'],
            is_main=rc['is_main']
        ) for rc in df]
        ProductImages.objects.bulk_create(model_objs)
        print(f'✅ {ProductImages.__name__}')
    except Exception as e:
        print(f'❌ {ProductImages.__name__} - {e}')

insert_address()
insert_category()

########################
# user - vendor - customer
########################
def create_vendor_with_jwt(email, password, name, phone, description):
    user = User.objects.create_user(
        email=email,
        password=password,  # No need to hash the password here
        is_vendor=True,
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

def create_customer_with_jwt(email, password, fullname, phone, date_of_birth):
    user = User.objects.create_user(
        email=email,
        password=password,  # No need to hash the password here
        is_customer=True,
    )
    cart = Cart.objects.create()
    customer = Customer.objects.create(
        user=user,
        fullname=fullname,
        phone=phone,
        date_of_birth=date_of_birth,
        cart = cart,
        age = 2024 - int(date_of_birth.split('-')[0])
    )
    province = Province.objects.get(province_id=79)
    district = District.objects.get(province_id=province, district_id=764)
    ward = Ward.objects.get(district_id=district, ward_id=26899)
    Address.objects.create(
        province_id=province,
        district_id=district,
        ward_id=ward,
        address_detail='13/1 Phường 11, quận Gò Vấp, TP.HCM',
    )
    address = Address.objects.get(address_detail='13/1 Phường 11, quận Gò Vấp, TP.HCM')
    user.address = address
    user.save()
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    
    # Cart.objects.create(customer=customer)
    
    return user, customer, access_token, refresh_token

user1, vendor1, token1, refresh1 = create_vendor_with_jwt(
    email='minhlong2002@gmail.com',
    password='123',  # Pass the plain password
    name='Minh Long',
    phone='1234567890',
    description='This is a description for Vendor One.'
)
print(f'✅ Vendor: {user1.email}, Access Token: {token1}, Refresh Token: {refresh1}')

user2, customer2, token2, refresh2 = create_customer_with_jwt(
    email='vanhau20022018@gmail.com',
    password='123',  # Pass the plain password
    fullname='Văn Hậu',
    phone='0987654321',
    date_of_birth='2002-02-20',
)

print(f'✅ Customer: {user2.email}, Access Token: {token2}, Refresh Token: {refresh2}')

user3, vendor3, token3, refresh3 = create_vendor_with_jwt(
    email='quachnam311@gmail.com',
    password='123',  # Pass the plain password
    name='Qx Nam',
    phone='0398089311',
    description='This is a description for Vendor Three.'
)
print(f'✅ Vendor: {user3.email}, Access Token: {token3}, Refresh Token: {refresh3}')

insert_product()
insert_product_image()

## vector database
from pydantic import BaseModel
import requests
from tqdm import tqdm
class InsertPointRequestBody(BaseModel):
    slug: str
    product_id: int
    product_name: str
    product_url: str
def init_qdrant():
    collection_name='product'
    res = requests.delete(f'https://qdrant-iuhkart.aiclubiuh.com/collections/delete?collection_name={collection_name}')
    res = requests.post(f'https://qdrant-iuhkart.aiclubiuh.com/collections/create?collection_name={collection_name}')
    df = pd.read_csv('../schema/Database/products.csv')
    df = df[['product_id', 'product_name', 'slug']]
    loop = tqdm(df.iterrows(), total=df.shape[0], desc='Inserting', colour='green')
    for _, iter in loop:
        request_body = InsertPointRequestBody(
            slug=iter['slug'],
            product_id=iter['product_id'],
            product_name=f"{iter['product_name']}",
            product_url=f"https://example.com/{iter['product_id']}"
        )
        json_body = request_body.json()
        res = requests.post(f'https://qdrant-iuhkart.aiclubiuh.com/collections/{collection_name}/insert',
                            data=json_body, 
                            headers={"Content-Type": "application/json"}
                )
        loop.set_postfix(status_code = 'success' if res.status_code == 201 else 'fail')

init_qdrant()