#!/usr/bin/env python3
import os
from dotenv import dotenv_values



config = {
    **dotenv_values(".env")
}

sample_query = {
    'show all table': "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE'",

}

db = postgres_tool.PostgresTool(config['HOST'], config['USER'], config['PORT'], config['PASSWORD'], config['DATABASE'])
db.test_connection()
db.create_schema(sql_path='./IUHKart.sql')
db.query(sql_query=sample_query['show all table'])
db.close()

