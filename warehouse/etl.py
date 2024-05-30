import pandas as pd
from postgres_tool import PostgresTool
from dotenv import load_dotenv
import os

load_dotenv()
config = {
    'host': os.environ.get('HOST_DP'),
    'port': os.environ.get('PORT_DP'),
    'user': os.environ.get('USER_DP'),
    'password':  os.environ.get('PASSWORD_DP'),
    'database': os.environ.get('NAME_DP')
}
pg = PostgresTool(**config)
pg.test_connection()
# pg.create_schema('../schema/DWH.sql')
# tables = ['fact_order_product','dim_order', 'fact_review', 'dim_customer', 'dim_product', 'dim_category', 'dim_vendor']
# pg.delete_table(tables)
print(pg.get_all_table())
pg.close()