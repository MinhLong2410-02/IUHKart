import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

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

def extract():
    pass