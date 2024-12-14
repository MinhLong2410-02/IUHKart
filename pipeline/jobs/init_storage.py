from utils import Postgres
import pandas as pd

pg = Postgres()

# tables = pg.get_all_table()
# print(tables)
# pg.delete(table_name="province", pk_id=3)

# province
# df_province = pd.read_csv("db/province.csv")
# pg.upserts(datas=[tuple(i) for i in df_province[["id", "province_name"]].values], table_name="province")
# data = pg.query("SELECT count(*) FROM province;", False)
# print(data)

# address
# df_address = pd.read_csv("db/address.csv")
# pg.upserts(datas=[tuple([int(i) for i in record]) for record in df_address[["id", "province_id"]].values], table_name="address")
# data = pg.query("SELECT count(*) FROM address;", False)
# print(data)

# category
# df_category = pd.read_csv("db/category.csv")
# pg.upserts(datas=[tuple(record) for record in df_category.values], table_name="category")
# data = pg.query("SELECT count(*) FROM category;", False)
# print(data)

# # product
# df_product = pd.read_csv("db/product.csv")
# pg.upserts(datas=[tuple([int(i) for i in record]) for record in df_product.values], table_name="product")
# data = pg.query("SELECT count(*) FROM product;", False)
# print(data)

# # orders
df_orders = pd.read_csv("db/orders.csv")
pg.upserts(datas=[tuple([int(i) for i in record]) for record in df_orders.values], table_name="orders")
data = pg.query("SELECT count(*) FROM orders;", False)
print(data)

# order_product
df_order_product = pd.read_csv("db/order_product.csv")
pg.upserts(datas=[tuple([int(i) for i in record]) for record in df_order_product.values], table_name="order_product")
data = pg.query("SELECT count(*) FROM order_product;", False)
print(data)

pg.close()