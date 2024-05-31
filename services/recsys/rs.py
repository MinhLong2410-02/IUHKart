import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import LabelEncoder
import os, redis, psycopg2, json
from sklearn.feature_extraction.text import TfidfVectorizer
from dotenv import load_dotenv
os.chdir(os.path.dirname(__file__))

def write_log(text):
    with open('logs/log.log', 'a', encoding='utf-8') as f:
        f.write(f'{text}' + '\n')

def get_data(config):
    query_string = '''
    select p.product_id, p.slug, p.category_id, p.ratings, p.original_price, p.stock from dim_product p'''

    connection = psycopg2.connect(
        dbname=config['database'],
        user=config['user'],
        password=config['password'],
        host=config['host'],
        port=config['port']
    )
    cursor = connection.cursor()
    cursor.execute(query_string)
    result = cursor.fetchall()
    meta_database = pd.DataFrame(result, columns=['product_id', 'slug', 'category_id', 'ratings', 'original_price', 'stock'])
   
    # drop in_use column
    # label_encoder = LabelEncoder()
    # for column in ['category_id']:
    #     meta_database[column] = label_encoder.fit_transform(meta_database[column])
    # print(meta_database.columns)
    return meta_database

class RS:
    def __init__(self, data):

        '''
        Recommend products from product id 
        Args:
            data: data had get from database 
            corr_name_products: correlation product names had compute by tfidf
            correlation_matrix: correlation properties of products multiply by corr_name_products
            
        '''
        self.data = data.set_index('product_id')
        self.tfidf_name_products()
        self.normalization_data()

    def tfidf_name_products(self):
        vectorizer = TfidfVectorizer()
        tfidf = vectorizer.fit_transform(self.data.slug)
        self.corr_name_products = np.corrcoef(tfidf.toarray())


    def normalization_data(self):
        print(self.data.shape)
        SVD = TruncatedSVD(n_components=4)
        decomposed_matrix = SVD.fit_transform(self.data.drop(columns=['slug']))
        self.compute_corr(decomposed_matrix)

    def compute_corr(self, decomposed_matrix):
        correlation_matrix = np.corrcoef(decomposed_matrix) * self.corr_name_products 
        self.correlation_matrix = correlation_matrix

    def update(self, data):
        self.data = data.set_index('product_id')
        self.normalization_data()
    def recommend(self, product_id, number_of_rs = 20):
        '''
        Args:
            recommend: list of product id had recommend
        
        '''
        product_names = list(self.data.index)
        product_ID = product_names.index(product_id)
        correlation_product_ID = self.correlation_matrix[: , product_ID]

        # Sorted id with corr highest according to descrease
        top_two_indices = np.argsort(correlation_product_ID)[-number_of_rs:]
        top_two_indices = np.flip(top_two_indices)

        # get id 
        recommend = list(self.data.index[top_two_indices])
        
        return recommend

if __name__ == "__main__":
    load_dotenv()
    olap_config = {
        'host': os.environ.get('DWHOST'),
        'port': os.environ.get('PORT'),
        'user': os.environ.get('DWUSER'),
        'password':  os.environ.get('PASSWORD'),
        'database': os.environ.get('NAME')
    }
    oltp_config = {
        'host': os.environ.get('HOST'),
        'port': os.environ.get('PORT'),
        'user': os.environ.get('USER'),
        'password':  os.environ.get('PASSWORD'),
        'database': os.environ.get('NAME')
    }
    # write_log(config)
    write_log('Recommendation service is running')
    # pubsub
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', 6379))
    redis_db = int(os.getenv('REDIS_DB', 0))
    redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    pubsub = redis_client.pubsub()
    pubsub.subscribe('recommendation')
    try:
        for message in pubsub.listen():
            if message['type'] == 'message':
                json_string = message['data'].decode('utf-8')
                write_log(json_string)
                json_data = json.loads(json_string)
                
                user_id = json_data['user_id']
                product_id = json_data['product_id']
                rs = RS(get_data(olap_config))
                product_ids = rs.recommend(product_id)
                del rs
                product_ids.append(user_id)
                query_string = '''UPDATE customer
                    SET recommend_product_ids  = '{%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s}'
                    WHERE WHERE user_id = %s;
                ''', 
                connection = psycopg2.connect(
                    dbname=oltp_config['NAME'],
                    user=oltp_config['USER'],
                    password=oltp_config['PASSWORD'],
                    host=oltp_config['HOST'],
                    port=oltp_config['PORT']
                )
                cursor = connection.cursor()
                try:
                    cursor.execute(query_string, product_ids)
                    connection.commit()
                except Exception as e:
                    connection.rollback()
    except KeyboardInterrupt:
        redis_client.close()