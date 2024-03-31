#!/usr/bin/env python3
import os
from dotenv import dotenv_values
import postgres_tool
config = {
    **dotenv_values(".env")
}

sample_query = {
    'show all table': "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE'",

}

db = postgres_tool.PostgresTool(config['HOST'], config['USER'], config['PORT'], config['PASSWORD'], config['DATABASE'])
db.test_connection()
db.create_schema(sql_path='./e-commerce.sql')
db.query(sql_query=sample_query['show all table'])
# db.delete_table(table_names=['Review', 'Seller', 'OrderItem', 'Payment', 'Cart', 'Address', 'Order', 'Product', 'Customer', 'Category']) # delete: 'Review', 'Seller', 'OrderItem', 'Payment', 'Cart', 'Address', 'Order', 'Product', 'Customer', 'Category'
db.close()

