import psycopg2
from tabulate import tabulate
import pandas as pd
import numpy as np

class PostgresTool():
    def __init__(self, host, user, port, password, database):
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.database = database

        self.conn = None
        self.cursor = None
    
    def connect(self):
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            port=self.port,
            password=self.password
        )
        self.cursor = self.conn.cursor()
    
    def test_connection(self,):
        self.connect()
        if self.conn and self.cursor:
            print("✅ Connection established!")
        else:
            print("❌ Connection failed!")
    
    def close(self):
        self.cursor.close()
        self.conn.close()
        print("🖐 Closed connection")

    def query(self, sql_query):
        self.cursor.execute("ROLLBACK")
        self.cursor.execute(sql_query)
        rows = self.cursor.fetchall()
        # print(tabulate(rows, headers=[desc[0] for desc in self.cursor.description], tablefmt='psql'))
        df = pd.DataFrame(rows, columns=[desc[0] for desc in self.cursor.description])
        return df

    def create_schema(self, sql_path='*.sql'):
        with open(sql_path, 'r') as f:
            schema = f.read().split('\n\n')
        try:
            for statement in schema:
                self.cursor.execute(statement)
                if statement.find('CREATE TABLE') != -1:
                    print(f'''📢 Created table {statement.split('"')[1]}''')
                if statement.find('ALTER TABLE') != -1:
                    alter = statement.split('"')
                    print(f'''🔌 Linked table {alter[1]} -> {alter[5]}''')
            self.conn.commit()
        except Exception as e:
            print(f'❌ {e}')
        
    def get_columns(self, table_name):
        self.cursor.execute("ROLLBACK")
        self.cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{table_name}'".format(table_name=table_name))
        cols = [i[0] for i in self.cursor.fetchall()]
        return cols

    def get_all_table(self,):
        self.cursor.execute("ROLLBACK")
        self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE'")
        tables = [i[0] for i in self.cursor.fetchall()]
        return tables
    
    def delete_table(self, table_names = []):
        self.cursor.execute("ROLLBACK")
        for table in table_names:
            try:
                self.cursor.execute(f"DROP TABLE {table}")
                print(f"🗑 Deleted {table}")
            except Exception as e:
                print(f"❌ {e}")
        self.conn.commit()

    def push_data(self, df, table_name):
        self.cursor.execute("ROLLBACK")
        cols = self.get_columns(table_name)
        df = df[cols]
        datas = [tuple(i) for i in np.where(pd.isna(df), None, df).tolist()]
        sql_insert = f"insert into {table_name} ({','.join(cols)}) values ({','.join(['%s']*len(cols))})"
        self.cursor.executemany(sql_insert, datas)
        self.conn.commit()

    def truncate(self, table_name):
        self.cursor.execute("ROLLBACK")
        self.cursor.execute(f"TRUNCATE {table_name} CASCADE")
        self.conn.commit()