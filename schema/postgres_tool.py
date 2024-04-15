import psycopg2
from tabulate import tabulate


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
        # self.cur.execute("ROLLBACK")
        self.cursor.execute(sql_query)
        rows = self.cursor.fetchall()
        print(tabulate(rows, headers=[desc[0] for desc in self.cursor.description], tablefmt='psql'))

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
        # self.cursor.execute("ROLLBACK")
        self.cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{table_name}'".format(table_name=table_name))
        cols = [i[0] for i in self.cursor.fetchall()]
        return cols

    def get_all_table(self,):
        # self.cursor.execute("ROLLBACK")
        self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE'")
        tables = [i[0] for i in self.cursor.fetchall()]
        print(tables)
    
    def delete_table(self, table_names = []):
        self.cursor.execute(f"DROP TABLE {', '.join(table_names)}")
        print(f"🗑 Deleted")
        self.conn.commit()