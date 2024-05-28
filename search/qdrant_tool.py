from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import requests, os
from dotenv import load_dotenv
from uuid import uuid4
from tqdm import tqdm
# load_dotenv('./.env')

class QdrantTool:
    def __init__(self, url="https://qdrant-iuhkart.aiclubiuh.com/"):
        '''
        params:
        - {'path': name_db} for in locally
        - {'host': host, 'port': port} for in server
        - {'url': url} for in server
        '''
        self.client = QdrantClient(url)
        self.url_embedding = "http://9net.ddns.net:9008/embedding?q={text_embedding}"
        self.all_collection_name = [c.name for c in self.client.get_collections().collections]

    def reinit_collection(self, collection_name, embedding_size=384, distance=Distance.COSINE):
        self.collection_name = collection_name
        if collection_name in self.all_collection_name:
            self.client.delete_collection(collection_name)
            
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=embedding_size, distance=distance),
        )
        print('✅ init collection success')
    
    def insert(self, df):
        loop = tqdm(df.iterrows(), desc="Inserting", total=df.shape[0])
        for _, it in loop:
            try:
                content = it.to_dict()
                rep = requests.get(self.url_embedding.format(text_embedding=content['slug']))
                vector = rep.json()['embedding']
                point = PointStruct(id=str(uuid4()),
                                    vector=vector,
                                    payload=content
                        )
                self.client.upsert(collection_name=self.collection_name, points=[point])
                loop.set_postfix({"Status": "✅ Success"})
            except Exception as e:
                loop.set_postfix({"❌ Error": str(e)})
                continue

    def search(self, prompt, limit=1):
        try:
            prompt_embedding = requests.get(self.url_embedding.format(text_embedding=prompt)).json()['embedding']
            results = self.client.search(collection_name=self.collection_name, query_vector=prompt_embedding, limit=limit)
            return [i.model_dump() for i in results]
        except Exception as e:
            return str(e)
        
    def close(self,):
        self.client.close()
        print('👋 bye')

if __name__=='__main__':
    print(os.getenv('QDRANT_URL'))