from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import os, requests
from dotenv import load_dotenv
TEXT_EMBEDDING_URL = os.getenv('TEXT_EMBEDDING_URL')
HOST = os.getenv('HOST')
HOST = 'http://crawl.serveftp.com'
PORT = 6334

def getTextEmbedding(text: str):
    response = requests.get(TEXT_EMBEDDING_URL + text)
    vector = response.json()['embedding'] if response.status_code == 200 else None
    return vector

def init_qdrant():
    collection_name='product'
    client = QdrantClient(url=HOST, port=PORT)
    if collection_name in [c.name for c in client.get_collections().collections]:
        client.delete_collection(collection_name=collection_name)
    client.create_collection(collection_name=collection_name, vectors_config=VectorParams(size=384, distance=Distance.COSINE))

init_qdrant()

###
from iuhkart.wsgi import *
from iuhkart.settings import *
from django.contrib.auth import get_user_model
from apps.product.models import Category, Product, ProductImages
from apps.account.models import Vendor, Customer, User
from apps.address.models import Province, District, Ward, Address
from apps.cart.models import Cart
from apps.discount.models import Discount, OrderProductDiscount
from apps.order.models import OrderProduct, Order, Transaction
from apps.review.models import Review

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
DB_USER = os.getenv('DBUSER')
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

# Delete all tables in public schema
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
os.system('sh migrate.sh')
try:
    os.system('migrate.bat')
except:
    pass    
path = {
    'province': 'https://raw.githubusercontent.com/MinhLong2410-02/VN-province-api-test/main/province.csv',
    'district': 'https://raw.githubusercontent.com/MinhLong2410-02/VN-province-api-test/main/district.csv',
    'ward': 'https://raw.githubusercontent.com/MinhLong2410-02/VN-province-api-test/main/ward.csv',
    'category': '../schema/Database/categories.csv',
    'product': '../schema/Database/products.csv',
    'product_image': '../schema/Database/product_images.csv',
    'product_image_main': '../schema/Database/product_images_main.csv',
    'discount': '../schema/Database/discount_new.csv',
    'product_discount': '../schema/Database/product_discount.csv',
    'order_products': '../schema/Database/order_products.csv',
    'orders': '../schema/Database/orders.csv',
    'review': '../schema/Database/reviews.csv',
    'transaction': '../schema/Database/transactions.csv',
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
            ratings=rc['ratings'],
            date_add=rc['date_add'],
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
        df.columns = ['product_image_id', 'product_id', 'image_url', 'is_main']
        df = df.to_dict('records')
        product_cache = {x.product_id: x for x in Product.objects.all()}

        model_objs = [ProductImages(
            # product_image_id=rc['product_image_id'],
            product_id=product_cache[rc['product_id']],
            image_url=rc['image_url'].split('product/')[-1],
            is_main=rc['is_main']
        ) for rc in df]
        ProductImages.objects.bulk_create(model_objs)
        print(f'✅ {ProductImages.__name__}')
    except Exception as e:
        print(f'❌ {ProductImages.__name__} - {e}')

insert_address()
insert_category()

########################
# user - Shop - customer - address
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

##--------------------- Shop 
user1, vendor1, token1, refresh1 = create_vendor_with_jwt(
    email='minhlong2002@gmail.com',
    password='123',  # Pass the plain password
    name='Minh Long',
    phone='1234567890',
    description='This is a description for Vendor One.'
)
print(f'✅ Vendor: {user1.email}, Access Token: {token1}, Refresh Token: {refresh1}')

user2, vendor2, token2, refresh2 = create_vendor_with_jwt(
    email='quachnam311@gmail.com',
    password='123',  # Pass the plain password
    name='Qx Nam',
    phone='0398089311',
    description='This is a description for Vendor Three.'
)
print(f'✅ Vendor: {user2.email}, Access Token: {token2}, Refresh Token: {refresh2}')

##--------------------- Customer
address = create_address(79, 764, 26899, '12 Nguyễn Văn Bảo, Phường 4, quận Gò Vấp, TP.HCM')
user3, customer3, token3, refresh3 = create_customer_with_jwt(
    email='vanhau20022018@gmail.com',
    password='123',  # Pass the plain password
    fullname='Văn Hậu',
    phone='0987654321',
    date_of_birth='2002-02-20',
    address=address
)
print(f'✅ Customer: {user3.email}, Access Token: {token3}, Refresh Token: {refresh3}')

address = create_address(79, 764, 26881, '273/34/1 Nguyễn Văn Đậu, Phường 11, Bình Thạnh, TP.HCM')
user4, customer4, token4, refresh4 = create_customer_with_jwt(
    email='lamthanhthanh@gmail.com',
    password='123',  # Pass the plain password
    fullname='Lê Thành Nghĩa',
    phone='0987654322',
    date_of_birth='2003-07-31',
    address=address
    
)
print(f'✅ Customer: {user4.email}, Access Token: {token4}, Refresh Token: {refresh4}')

address = create_address(79, 764, 26898, '185b Nguyễn Oanh, Phường 10, Gò Vấp, Hồ Chí Minh')
user5, customer5, token5, refresh5 = create_customer_with_jwt(
    email='nhanvi212@gmail.com',
    password='123',  # Pass the plain password
    fullname='Lưu Lương Vi Nhân',
    phone='0987654324',
    date_of_birth='2002-03-20',
    address=address
    
)
print(f'✅ Customer: {user5.email}, Access Token: {token5}, Refresh Token: {refresh5}')

address = create_address(79, 764, 26898, '190 Đ. Quang Trung, Phường 10, Gò Vấp, Hồ Chí Minh')
user6, customer6, token6, refresh6 = create_customer_with_jwt(
    email='hungcao@gmail.com',
    password='123',  # Pass the plain password
    fullname='Cao Nguyễn Gia Hưng',
    phone='0987654324',
    date_of_birth='2002-03-20',
    address=address
    
)
print(f'✅ Customer: {user6.email}, Access Token: {token6}, Refresh Token: {refresh6}')

print(f'✅ Create a fake address acount with address_id: {address.address_id}')
insert_product()
insert_product_image()
#---------------------

# order
def create_discount():
    try:
        df = pd.read_csv(path['discount'])
        product_cache = {x.product_id: x for x in Product.objects.all()}
        # convert to dict
        df = df.to_dict('records')
        model_objs = [Discount(
            discount_id=rc['discount_id'],
            # product=product_cache[rc['product_id']],
            name=rc['name'],
            discount_percent=rc['discount_percent'],
            # start_date=rc['start_date'],
            # end_date=rc['end_date'],
            # vendor = Product.objects.get(product_id=rc['product_id']).created_by
        ) for rc in df]
        Discount.objects.bulk_create(model_objs)
        print(f'✅ {Discount.__name__}')
    except Exception as e:
        print(f'❌ {Discount.__name__} - {e}')

def create_product_discount():
    try:
        df = pd.read_csv(path['product_discount'])
        # convert to dict
        discount_cache = {x.discount_id: x for x in Discount.objects.all()}
        product_cache = {x.product_id: x for x in Product.objects.all()}
        df = df.to_dict('records')
        model_objs = [OrderProductDiscount(
            product_discount_id=rc['product_discount_id'],
            product=product_cache[rc['product_id']],
            discount=discount_cache[rc['discount_id']],
            start_date=rc['start_date'],
            end_date=rc['end_date']
        ) for rc in df]
        OrderProductDiscount.objects.bulk_create(model_objs)
        print(f'✅ {OrderProductDiscount.__name__}')
    except Exception as e:
        print(f'❌ {OrderProductDiscount.__name__} - {e}')

create_discount()
create_product_discount()

def create_review():
    try:
        df = pd.read_csv(path['review'])
        # convert to dict
        customer_cache = {x.id: x for x in Customer.objects.all()}
        product_cache = {x.product_id: x for x in Product.objects.all()}
        df = df.to_dict('records')
        model_objs = [Review(
            review_id = rc['review_id'],
            product_id = product_cache[rc['product_id']],
            customer_id = customer_cache[rc['customer_id']],
            review_rating = rc['review_rating'],
            review_date = rc['review_date'],
            review_content = rc['review_content']
        ) for rc in df]
        Review.objects.bulk_create(model_objs)
        print(f'✅ {Review.__name__}')
    except Exception as e:
        print(f'❌ {Review.__name__} - {e}')

create_review()

def create_order():
    try:
        df = pd.read_csv(path['orders'])
        # convert to dict
        customer_cache = {x.id: x for x in Customer.objects.all()}
        address_cache = {x.address_id: x for x in Address.objects.all()}
        df = df.to_dict('records')
        model_objs = [Order(
            order_id = rc['order_id'],
            order_number = rc['order_number'],
            shipping_date = rc['shipping_date'],
            order_date = rc['order_date'],
            order_status = rc['order_status'],
            order_total = rc['total_price'],
            customer = customer_cache[rc['customer_id']],
            address = address_cache[rc['address_id']]
        ) for rc in df]
        Order.objects.bulk_create(model_objs)
        print(f'✅ {Order.__name__}')
    except Exception as e:
        print(f'❌ {Order.__name__} - {e}')

def create_order_product():
    try:
        df = pd.read_csv(path['order_products'])
        # convert to dict
        order_cache = {x.order_id: x for x in Order.objects.all()}
        product_cache = {x.product_id: x for x in Product.objects.all()}
        df = df.to_dict('records')
        model_objs = [OrderProduct(
            order_product_id=rc['order_product_id'],
            order=order_cache[rc['order_id']],
            product=product_cache[rc['product_id']],
            quantity=rc['quantity'],
            price=rc['price']
        ) for rc in df]
        OrderProduct.objects.bulk_create(model_objs)
        print(f'✅ {OrderProduct.__name__}')
    except Exception as e:
        print(f'❌ {OrderProduct.__name__} - {e}')

create_order()
create_order_product()


def create_transaction():
    try:
        df = pd.read_csv(path['orders'])
        # convert to dict
        customer_cache = {x.id: x for x in Customer.objects.all()}
        df = df.to_dict('records')
        model_objs = [Transaction(
            transaction_id = rc['order_id'],
            order = Order.objects.get(order_id=rc['order_id']),
            transation_date = rc['order_date'],
            total_money = rc['total_price'],
            status = 'completed',
            customer = customer_cache[rc['customer_id']]
        ) for rc in df]
        Transaction.objects.bulk_create(model_objs)
        print(f'✅ {Transaction.__name__}')
    except Exception as e:
        print(f'❌ {Transaction.__name__} - {e}')

create_transaction()


