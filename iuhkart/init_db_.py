from iuhkart.wsgi import *
from iuhkart.settings import *
from django.contrib.auth import get_user_model
from apps.product.models import Category, Product, ProductImages
from apps.account.models import Vendor, Customer, User
from apps.address.models import Province, District, Ward, Address
from apps.cart.models import Cart

import pandas as pd
import numpy as np
import random, psycopg2
from dotenv import load_dotenv
import os
from rest_framework_simplejwt.tokens import RefreshToken
import ssl
import requests
from tqdm import tqdm

ssl._create_default_https_context = ssl._create_stdlib_context

load_dotenv('.env')
PROJECT_STATUS = environ.get('STATUS')
DB_NAME = os.getenv('NAME')
DB_USER = os.getenv('USER')
DB_PASS = os.getenv('PASSWORD')
DB_HOST = 'localhost' if PROJECT_STATUS == 'DEV' else os.getenv('HOST')
DB_PORT = os.getenv('PORT')
print(F'✅ STATUS: {PROJECT_STATUS}')
connection = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

connection.autocommit = True
cursor = connection.cursor()

# Execute a simple SQL query
cursor.execute('''DO $$ 
DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END $$;''')

print(cursor.statusmessage)
cursor.close()
connection.close()

os.system('migrate.bat')
path = {
    'province': 'https://raw.githubusercontent.com/MinhLong2410-02/VN-province-api-test/main/province.csv',
    'district': 'https://raw.githubusercontent.com/MinhLong2410-02/VN-province-api-test/main/district.csv',
    'ward': 'https://raw.githubusercontent.com/MinhLong2410-02/VN-province-api-test/main/ward.csv',
    'category': '../schema/Database/categories.csv',
    'product': '../schema/Database/products.csv',
    'product_image': '../schema/Database/product_images.csv',
    'product_image_main': '../schema/Database/product_images_main.csv',
    
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

def assign_is_main(group):
    num_images = len(group)
    if num_images <= 3:
        group['is_main'] = True
    else:
        main_indices = np.random.choice(group.index, 3, replace=False)
        group['is_main'] = False
        group.loc[main_indices, 'is_main'] = True
    return group
def insert_product_image():
    try:
        df = pd.read_csv(path['product_image_main'])
        # process
        # df.drop_duplicates(subset=['product_img_id', 'product_id'], inplace=True)
        # df = df.groupby('product_id', group_keys=False).apply(assign_is_main)
        df.columns = ['product_image_id', 'product_id', 'image_url', 'is_main']
        # df.to_csv('../schema/Database/product_images_main.csv', index=False)
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
# user - vendor - customer - address
########################
def create_address(province_id, district_id, ward_id, address_detail):
    province = Province.objects.get(province_id=province_id)
    district = District.objects.get(province_id=province, district_id=district_id)
    ward = Ward.objects.get(district_id=district, ward_id=ward_id)
    address = Address.objects.create(
        province_id=province,
        district_id=district,
        ward_id=ward,
        address_detail=address_detail,
    )
    return address

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

def create_customer_with_jwt(email, password, fullname, phone, date_of_birth, address):
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

address = create_address(79, 764, 26899, '13/1 Phường 11, đường Nguyễn Văn Hậu, quận Gò Vấp, TP.HCM')
user2, customer2, token2, refresh2 = create_customer_with_jwt(
    email='vanhau20022018@gmail.com',
    password='123',  # Pass the plain password
    fullname='Văn Hậu',
    phone='0987654321',
    date_of_birth='2002-02-20',
    address=address
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

address = create_address(79, 764, 26881, '69/96 Phường 12, đường Lê Thành Nghĩa, quận Gò Vấp, TP.HCM')
user4, customer4, token4, refresh4 = create_customer_with_jwt(
    email='nguyenvannam14056969@gmail.com',
    password='123',  # Pass the plain password
    fullname='Nguyễn VNam',
    phone='0987654322',
    date_of_birth='2003-07-31',
    address=address
    
)
print(f'✅ Customer: {user4.email}, Access Token: {token4}, Refresh Token: {refresh4}')


address = create_address(79, 764, 26898, '69/96 Phường 79, đường Nhân Vi, quận Gò Vấp, TP.HCM')
user5, customer5, token5, refresh5 = create_customer_with_jwt(
    email='nhanvi212@gmail.com',
    password='123',  # Pass the plain password
    fullname='Lưu Lương Vi Nhân',
    phone='0987654324',
    date_of_birth='2002-03-20',
    address=address
    
)
print(f'✅ Customer: {user5.email}, Access Token: {token5}, Refresh Token: {refresh5}')


insert_product()
insert_product_image()

## vector database
def init_qdrant():
    broken_products = []
    collection_name='product'
    requests.delete(f'https://qdrant-iuhkart.aiclubiuh.com/collections/delete?collection_name={collection_name}')
    requests.post(f'https://qdrant-iuhkart.aiclubiuh.com/collections/create?collection_name={collection_name}')
    df = pd.read_csv('../schema/Database/products.csv')
    product_image_df = pd.read_csv('../schema/Database/product_images_main.csv')
    df = df[['product_id', 'product_name', 'slug']]
    loop = tqdm(df.iterrows(), total=df.shape[0], desc='Insert to qdrantDB', colour='green')
    for _, iter in loop:
        product_image = product_image_df[(product_image_df['product_id']==iter['product_id']) & (product_image_df['is_main']==True)]
        if product_image.shape[0] == 0:
            broken_products.append((iter['product_id'], iter['product_name']))
            continue
        image_url = product_image['image_url'].values[0]
        request_body = {
            'slug': iter['slug'],
            'product_id': iter['product_id'],
            'product_name': f"{iter['product_name']}",
            'product_image_url': image_url
        }
        res = requests.post(f'https://qdrant-iuhkart.aiclubiuh.com/collections/{collection_name}/insert',
                            json=request_body,
                            headers={"Content-Type": "application/json"}
                )
        loop.set_postfix(status_code='success' if res.status_code == 201 else 'fail')
    df = pd.DataFrame(broken_products, columns=['product_id', 'product_name'])
    df.to_csv('../schema/Database/broken_products.csv', index=False)
# init_qdrant()