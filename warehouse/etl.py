import pandas as pd
import psycopg2
from dotenv import load_dotenv
from postgres_tool import PostgresTool
import os
import warnings
warnings.filterwarnings("ignore")

load_dotenv()
configs = {
    'DB': {
        'host': os.environ.get('HOST_DP'),
        'port': os.environ.get('PORT_DP'),
        'user': os.environ.get('USER_DP'),
        'password': os.environ.get('PASSWORD_DP'),
        'database': os.environ.get('NAME_DP')
    },
    'WH': {
        'host': os.environ.get('HOST_DWH'),
        'port': os.environ.get('PORT_DWH'),
        'user': os.environ.get('USER_DWH'),
        'password': os.environ.get('PASSWORD_DWH'),
        'database': os.environ.get('NAME_DWH')
    }
    
}

select_columns_query = '''
SELECT column_name 
FROM information_schema.columns 
WHERE table_schema = 'public' AND table_name = '{table_name}'
'''

extract_query_product = '''
SELECT *
FROM public.product
WHERE date_created > current_date - interval '1 days';
'''

extract_query_vendor = '''
SELECT *
FROM public.vendor
WHERE date_join > current_date - interval '1 days';
'''

extract_query_category = '''
SELECT *
FROM public.category
'''

extract_query_customer = '''
SELECT *
FROM public.customer
WHERE date_join > current_date - interval '1 days';
'''

extract_query_order = '''
SELECT *
FROM public.order
WHERE order_date > current_date - interval '1 days';
'''

extract_query_review = '''
SELECT *
FROM public.review
WHERE review_date > current_date - interval '1 days';
'''

extract_query_order_product ='''
SELECT *
FROM public.order_product
WHERE order_id in ({oids});
'''

def main():
    pg1 = PostgresTool(**configs['DB'])
    pg1.test_connection()
    pg2 = PostgresTool(**configs['WH'])
    pg2.test_connection()

    try:
        table_name = 'dim_vendor'
        df = pg1.query(extract_query_vendor)
        df = df.rename(columns={'id': 'vendor_id'})
        pg2.truncate(table_name)
        pg2.push_data(df, table_name)
        print('✅ dim_vendor')
    except Exception as e:
        print('❌ dim_vendor:', e)

    try:
        table_name = 'dim_category'
        df = pg1.query(extract_query_category)
        pg2.truncate(table_name)
        pg2.push_data(df, table_name)
        print('✅ dim_category')
    except Exception as e:
        print('❌ dim_category:', e)

    try:
        table_name = 'dim_product'
        df = pg1.query(extract_query_product)
        pg2.truncate(table_name)
        pg2.push_data(df, table_name)
        print('✅ dim_product')
    except Exception as e:
        print('❌ dim_product:', e)

    try:
        table_name = 'dim_customer'
        df = pg1.query(extract_query_customer)
        df = df.rename(columns={'id': 'customer_id'})
        pg2.truncate(table_name)
        pg2.push_data(df, table_name)
        print('✅ dim_customer')
    except Exception as e:
        print('❌ dim_customer:', e)

    try:
        table_name = 'fact_review'
        df = pg1.query(extract_query_review)
        pg2.truncate(table_name)
        pg2.push_data(df, table_name)
        print('✅ fact_review')
    except Exception as e:
        print('❌ fact_review:', e)

    ids = []
    try:
        table_name = 'dim_order'
        df = pg1.query(extract_query_order)
        ids = df['order_id'].tolist()
        pg2.truncate(table_name)
        pg2.push_data(df, table_name)
        print('✅ dim_order')
    except Exception as e:
        print('❌ dim_order:', e)
    
    try:
        table_name = 'fact_order_product'
        oids = ','.join([str(i) for i in ids])
        query = extract_query_order_product.format(oids=oids)
        df = pg1.query(query)
        pg2.truncate(table_name)
        pg2.push_data(df, table_name)
        print('✅ fact_order_product')
    except Exception as e:
        print('❌ fact_order_product:', e)

    pg1.close()
    pg2.close()

main()