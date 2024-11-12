import psycopg2
import pandas as pd
import random

# # Thông tin kết nối tới PostgreSQL
# conn_info = {
#     "host": "crawl.serveftp.com",
#     "port": "5567",
#     "database": "postgres",
#     "user": "iuhkart",
#     "password": "iuhkartpassword"
# }

# # Kết nối tới cơ sở dữ liệu
# conn = psycopg2.connect(**conn_info)
# cursor = conn.cursor()

# # Đóng kết nối
# cursor.close()
# conn.close()

# # Truy vấn để lấy tất cả các bảng trong schema public
# query = """
#     SELECT table_name
#     FROM information_schema.tables
#     WHERE table_schema = 'public'
#     AND table_type = 'BASE TABLE';
# """

# cursor.execute(query)
# tables = cursor.fetchall()
# tables = [table[0] for table in tables]
# print(tables)

# # Thực hiện truy vấn
# df = None
# for table_name in ["discounts"]:
#     query = f"SELECT * FROM {table_name};"
#     cursor.execute(query)
#     columns = [desc[0] for desc in cursor.description]
#     data = cursor.fetchall()

#     # Chuyển kết quả thành DataFrame
#     df = pd.DataFrame(data, columns=columns)
#     # df.to_csv(f'./data/{table_name}.csv', index=False)
# df.to_csv("d.csv", index=False)

# # categories
# df = pd.read_csv('web/schema/Database/categories.csv', index_col=0)
# df.to_csv('./data/categories.csv', index=False)

# # products
# df = pd.read_csv('web/schema/Database/products.csv', index_col=0)
# df.to_csv('./data/products.csv', index=False)

# # reviews
# df = pd.read_csv('web/schema/Database/review.csv', index_col=0)
# df = df.dropna(subset=['review_content'])
# df.to_csv('./data/reviews.csv', index=False)

# # categories
# df = pd.read_csv('web/schema/Database/categories.csv', index_col=0)
# df.to_csv('./data/categories.csv', index=False)

# # discount
# df = pd.read_csv('data/discounts.csv')
# df_p = pd.read_csv('data/products.csv')
# df_p = df_p.sample(frac=0.5)
# df_p = df_p[['product_id', 'vendor_id']]
# df_p['name'] = [random.choices(["flash sale", "sale"])[0] for _ in range(len(df_p))]
# df_p['discount_percent'] = [random.choices(range(2, 11))[0] for _ in range(len(df_p))]
# df_p['date_created'] = "2024-01-01 00:00:00"
# df_p['start_date'] = "2024-01-01 00:00:00"
# df_p['end_date'] = "2025-01-01 00:00:00"
# df_p['in_use'] = True
# df_p['discount_id'] = [i for i in range(len(df_p))]
# df_p = df_p[['discount_id', 'name', 'discount_percent', 'date_created', 'start_date', 'end_date', 'in_use', 'product_id', 'vendor_id']]
# df_p.to_csv('./data/discounts.csv', index=False)

def _get_price(product_id):
    df_p = pd.read_csv('./data/products.csv')
    df_d = pd.read_csv('./data/discounts.csv')
    price = df_p[df_p['product_id'] == product_id]['original_price'].values[0]
    discount = df_d[df_d['product_id'] == product_id]
    if len(discount) == 0:
        return price
    if discount['in_use'].values[0] == False:
        return price
    discount = discount['discount_percent'].values[0]
    return price * (1 - discount / 100)

def _get_random_date(start_date=None):
    date_range = pd.date_range(start='2024-01-01', end='2024-11-11', freq='D')
    random_date = date_range.to_series().sample(n=1).iloc[0]
    if start_date:
        date_range = pd.date_range(start=start_date, end='2024-11-11', freq='D')
        random_date = date_range.to_series().sample(n=1).iloc[0]
    return random_date.strftime('%Y-%m-%d')

def gen_order(n=1):
    df_p = pd.read_csv('./data/products.csv')
    df_o = pd.read_csv('./data/orders.csv')
    df_op = pd.read_csv('./data/order_products.csv')
    df_t = pd.read_csv('./data/transactions.csv')
    o_id = len(df_o)
    op_id = len(df_op)
    t_id = len(df_t)
    new_orders = []
    new_order_products = []
    new_transactions = []
    for i in range(n):
        n_product = random.randint(1, 3)
        product_ids = random.choices(df_p['product_id'], k=n_product)
        total_price = 0
        for product_id in product_ids:
            quantity = random.randint(1, 3)
            price = _get_price(product_id)
            new_order_products.append([op_id, quantity, price, o_id, product_id])
            total_price += price * quantity
            op_id += 1

        # order_id,order_number,shipping_date,order_date,order_status,order_total,total_price,address_id,customer_id
        start_date = _get_random_date()
        shipping_date = _get_random_date(start_date)
        status = random.choices(['completed', 'completed', 'completed', 'completed', 'completed', 'completed', 'cancelled'])[0]
        new_orders.append([o_id, o_id, start_date, shipping_date, status, n_product, total_price, random.randint(1, 4), random.randint(1, 3)])
        
        # transaction_id,transation_date,total_money,status,customer_id,order_id
        status = 'completed' if status == 'completed' else 'failed'

        new_transactions.append([t_id, _get_random_date(shipping_date), total_price, status, random.randint(1, 4), o_id])
        t_id += 1
        o_id += 1

    df_orders = pd.DataFrame(new_orders, columns=['order_id', 'order_number', 'shipping_date', 'order_date', 'order_status', 'order_total', 'total_price', 'address_id', 'customer_id'])
    df_order_products = pd.DataFrame(new_order_products, columns=['order_product_id', 'quantity', 'price', 'order_id', 'product_id'])
    df_transactions = pd.DataFrame(new_transactions, columns=['transaction_id', 'transaction_date', 'total_money', 'status', 'customer_id', 'order_id'])
    
    df_orders.to_csv('./data/orders.csv', index=False, mode='a', header=False)
    df_order_products.to_csv('./data/order_products.csv', index=False, mode='a', header=False)
    df_transactions.to_csv('./data/transactions.csv', index=False, mode='a', header=False)
    
if __name__ == "__main__":
    gen_order(n=1000)