from dotenv import load_dotenv
import os
from postgres_tool import PostgresTool

load_dotenv()
config = {
    'host': os.environ.get('HOST_DWH'),
    'port': os.environ.get('PORT_DWH'),
    'user': os.environ.get('USER_DWH'),
    'password':  os.environ.get('PASSWORD_DWH'),
    'database': os.environ.get('NAME_DWH')
}

pg = PostgresTool(**config)
pg.test_connection()
# pg.create_schema('../schema/DWH.sql')
# tables = ['fact_order_product','dim_order', 'fact_review', 'dim_customer', 'dim_product', 'dim_category', 'dim_vendor']
# pg.delete_table(tables)
print(pg.get_all_table())
pg.close()