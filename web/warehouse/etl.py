from dotenv import load_dotenv
from postgres_tool import PostgresTool
from datetime import datetime
import pytz
import os
import warnings
warnings.filterwarnings("ignore")
os.chdir(os.path.dirname(__file__))
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
print(configs)

extract_query_product = '''
SELECT *
FROM public.product
WHERE date_add >= current_date - interval '1 days';
'''

extract_query_vendor = '''
SELECT *
FROM public.vendor
WHERE date_join >= current_date - interval '1 days';
'''

extract_query_category = '''
SELECT *
FROM public.category
'''

extract_query_customer = '''
SELECT *
FROM public.customer
WHERE date_join >= current_date - interval '1 days';
'''

extract_query_order = '''
SELECT *
FROM public.order
WHERE order_date >= current_date - interval '1 days';
'''

extract_query_review = '''
SELECT *
FROM public.review
WHERE review_date >= current_date - interval '1 days';
'''

extract_query_order_product ='''
SELECT *
FROM public.order_product
WHERE order_id in ({oids});
'''

def write_log(text):
    with open('logs/scheduler.log', 'a', encoding='utf-8') as f:
        f.write(f'{text}' + '\n')

def dim_vendor():
    pg1 = PostgresTool(**configs['DB'])
    pg1.test_connection()
    pg2 = PostgresTool(**configs['WH'])
    pg2.test_connection()

    table_name = 'dim_vendor'
    try:
        df = pg1.query(extract_query_vendor)
        if len(df) != 0:
            df = df.rename(columns={'id': 'vendor_id'})
            pg2.push_data(df, table_name)
            # pg2.to_sql(df, table_name)
            write_log(f'✅ {table_name} - {df.shape[0]} rows')
        else:
            write_log(f'✅ {table_name} - 0 rows')
    except Exception as e:
        print(f'❌ {table_name} - {e}')

    pg1.close()
    pg2.close()

def dim_category():
    pg1 = PostgresTool(**configs['DB'])
    pg1.connect()
    pg2 = PostgresTool(**configs['WH'])
    pg2.connect()

    table_name = 'dim_category'
    try:
        df = pg1.query(extract_query_category)
        # pg2.truncate(table_name)
        pg2.push_data(df, table_name)
        # pg2.to_sql(df, table_name)
        write_log(f'✅ {table_name} - {df.shape[0]} rows')
    except Exception as e:
        print(f'❌ {table_name} - {e}')

    pg1.close()
    pg2.close()

def dim_product():
    pg1 = PostgresTool(**configs['DB'])
    pg1.connect()
    pg2 = PostgresTool(**configs['WH'])
    pg2.connect()

    table_name = 'dim_product'
    try:
        df = pg1.query(extract_query_product)
        if len(df) != 0:
            del df['date_created']
            df.rename(columns={'date_add': 'date_created'}, inplace=True)
            pg2.push_data(df, table_name)
            # pg2.to_sql(df, table_name)
            write_log(f'✅ {table_name} - {df.shape[0]} rows')
        else:
            write_log(f'✅ {table_name} - 0 rows')
    except Exception as e:
        print(f'❌ {table_name} - {e}')

    pg1.close()
    pg2.close()

def dim_customer():
    pg1 = PostgresTool(**configs['DB'])
    pg1.connect()
    pg2 = PostgresTool(**configs['WH'])
    pg2.connect()

    table_name = 'dim_customer'
    try:
        df = pg1.query(extract_query_customer)
        if len(df) != 0:
            df = df.rename(columns={'id': 'customer_id'})
            pg2.push_data(df, table_name)
            # pg2.to_sql(df, table_name)
            write_log(f'✅ {table_name} - {df.shape[0]} rows')
        else:
            write_log(f'✅ {table_name} - 0 rows')
    except Exception as e:
        print(f'❌ {table_name} - {e}')

    pg1.close()
    pg2.close()

def fact_review():
    pg1 = PostgresTool(**configs['DB'])
    pg1.connect()
    pg2 = PostgresTool(**configs['WH'])
    pg2.connect()

    table_name = 'fact_review'
    try:
        df = pg1.query(extract_query_review)
        if len(df) != 0:
            pg2.push_data(df, table_name)
            # pg2.to_sql(df, table_name)
            write_log(f'✅ {table_name} - {df.shape[0]} rows')
        else:
            write_log(f'✅ {table_name} - 0 rows')
    except Exception as e:
        print(f'❌ {table_name} - {e}')

    pg1.close()
    pg2.close()

def dim_order() -> list:
    pg1 = PostgresTool(**configs['DB'])
    pg1.connect()
    pg2 = PostgresTool(**configs['WH'])
    pg2.connect()

    table_name = 'dim_order'
    ids = []
    try:
        df = pg1.query(extract_query_order)
        if len(df) != 0:
            ids = df['order_id'].tolist()
            pg2.push_data(df, table_name)
            # pg2.to_sql(df, table_name)
            write_log(f'✅ {table_name} - {df.shape[0]} rows')
        else:
            write_log(f'✅ {table_name} - 0 rows')
    except Exception as e:
        print(f'❌ {table_name} - {e}')

    pg1.close()
    pg2.close()

    return ids

def fact_order_product(ids:list=[]):
    pg1 = PostgresTool(**configs['DB'])
    pg1.connect()
    pg2 = PostgresTool(**configs['WH'])
    pg2.connect()

    table_name = 'fact_order_product'
    try:
        if len(ids) == 0:
            write_log(f'✅ {table_name} - 0 rows')
        else:
            oids = ','.join([str(i) for i in ids])
            query = extract_query_order_product.format(oids=oids)
            df = pg1.query(query)
            if len(df) != 0:
                pg2.push_data(df, table_name)
                # pg2.to_sql(df, table_name)
                write_log(f'✅ {table_name} - {df.shape[0]} rows')
            else:
                write_log(f'✅ {table_name} - 0 rows')
    except Exception as e:
        print(f'❌ {table_name} - {e}')

    pg1.close()
    pg2.close()

    return ids

def main():
    dim_vendor()
    dim_category()
    dim_product()
    dim_customer()
    fact_review()
    ids = dim_order()
    fact_order_product(ids)

if __name__ == '__main__':
    write_log(f"Start {datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))}")
    main()
    write_log('-'*30)

    # print(configs)
    # write_log(configs)
    