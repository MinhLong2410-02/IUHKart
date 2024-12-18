from utils import Postgres
import pandas as pd

pg = Postgres()

# tables = pg.get_all_table()
# print(tables)
# pg.delete(table_name="province", pk_id=3)

# province
df_province = pd.read_csv("db/province.csv")
pg.upserts(datas=[tuple(i) for i in df_province[["id", "province_name"]].values], table_name="province")
data = pg.query("SELECT count(*) FROM province;", False)
print(f'✅ Provice {data[0][0]}')

# address
df_address = pd.read_csv("db/address.csv")
pg.upserts(datas=[tuple([int(i) for i in record]) for record in df_address[["id", "province_id"]].values], table_name="address")
data = pg.query("SELECT count(*) FROM address;", False)
print(f'✅ address {data[0][0]}')

# users
df_users = pd.read_csv("db/users.csv")
pg.upserts(datas=[tuple([int(i) for i in record]) for record in df_users[["id", "address_id"]].values], table_name="users")
data = pg.query("SELECT count(*) FROM users;", False)
print(f'✅ Users {data[0][0]}')

# customer
df_users = pd.read_csv("db/customer.csv")
pg.upserts(datas=[tuple(record) for record in df_users[["id", "name", "user_id"]].values], table_name="customer")
data = pg.query("SELECT count(*) FROM customer;", False)
print(f'✅ Customer {data[0][0]}')

# store
df_users = pd.read_csv("db/store.csv")
pg.upserts(datas=[tuple(record) for record in df_users[["id", "name", "user_id"]].values], table_name="store")
data = pg.query("SELECT count(*) FROM store;", False)
print(f'✅ Store {data[0][0]}')

# category
df_category = pd.read_csv("db/category.csv")
pg.upserts(datas=[tuple(record) for record in df_category.values], table_name="category")
data = pg.query("SELECT count(*) FROM category;", False)
print(f'✅ category {data[0][0]}')

# product
df_product = pd.read_csv("db/product.csv")
pg.upserts(datas=[tuple([int(i) for i in record]) for record in df_product.values], table_name="product")
data = pg.query("SELECT count(*) FROM product;", False)
print(f'✅ Product {data[0][0]}')

# promotion
df_pp = pd.read_csv("db/promotion.csv")
pg.upserts(datas=[tuple(record) for record in df_pp.values], table_name="promotion")
data = pg.query("SELECT count(*) FROM promotion;", False)
print(f'✅ promotion {data[0][0]}')

# promotion_product
df_pp = pd.read_csv("db/promotion_product.csv")
pg.upserts(datas=[tuple([int(i) for i in record]) for record in df_pp.values], table_name="promotion_product")
data = pg.query("SELECT count(*) FROM promotion_product;", False)
print(f'✅ promotion_product {data[0][0]}')

# orders
df_orders = pd.read_csv("db/orders.csv")
pg.upserts(datas=[tuple(record) for record in df_orders.values], table_name="orders")
data = pg.query("SELECT count(*) FROM orders;", False)
print(f'✅ orders {data[0][0]}')

# order_product
df_order_product = pd.read_csv("db/order_product.csv")
pg.upserts(datas=[tuple(record) for record in df_order_product.values], table_name="order_product")
data = pg.query("SELECT count(*) FROM order_product;", False)
print(f'✅ order_product {data[0][0]}')

# order_product
df_dim_date = pd.read_csv("db/dim_date.csv")
pg.upserts(datas=[tuple(record) for record in df_dim_date.values], table_name="order_date")
data = pg.query("SELECT count(*) FROM order_date;", False)
print(f'✅ dim_date {data[0][0]}')

pg.close()