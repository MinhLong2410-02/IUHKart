from qdrant_client import models
from kafka import KafkaConsumer
import json, sys
import logging
from datetime import datetime, timedelta
from database import db, qdrant_client as client, update_recommendations_in_postgres
from configs import KAFKA_HOST, KAFKA_PORT, KAFKA_TOPIC
from pprint import pprint
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_user_behavior_weights(user_id: str):
    try:
        one_month_ago = datetime.utcnow() - timedelta(days=30)
        
        user_behaviors = db.behaviors.find({
            "user_id": user_id,
            "timestamp": {"$gte": one_month_ago} 
        })
        
        product_weights = {}
        for behavior in user_behaviors:
            product_id = behavior["product_id"]
            weight = behavior["weight"]
            product_weights[product_id] = product_weights.get(product_id, 0) + weight
        
        return product_weights
    except Exception as e:
        logger.error(f"Error fetching user behavior weights for user {user_id}: {e}")
        raise

def fetch_product_embedding(product_id):
    try:
        res = client.scroll(
            collection_name="product",
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="product_id",
                        match=models.MatchValue(value=product_id),
                    )
                ]
            ),
            limit=1,
            with_vectors=True
        )

        if res[0]:
            record = res[0][0]  
            if record.vector:
                return record.vector  
            else:
                raise ValueError(f"Vector missing for product_id {product_id}")
        else:
            raise ValueError(f"Product ID {product_id} not found in Qdrant")
    except Exception as e:
        logger.error(f"Error fetching product embedding for product_id {product_id}: {e}")
        raise
    

def compute_weighted_embedding(user_id: str):
    try:
        # Get weighted interactions
        product_weights = get_user_behavior_weights(user_id)
        logger.info(f'🟢 product_weights: {product_weights.items()}')
        # Fetch embeddings and apply weights
        weighted_embedding = None
        total_weight = 0

        for product_id, weight in product_weights.items():
            embedding = fetch_product_embedding(int(product_id))  # From Qdrant or MongoDB
            if weighted_embedding is None:
                weighted_embedding = [x * weight for x in embedding]
            else:
                weighted_embedding = [x + y * weight for x, y in zip(weighted_embedding, embedding)]
            total_weight += weight
        
        # Normalize the weighted embedding
        if total_weight > 0:
            weighted_embedding = [x / total_weight for x in weighted_embedding]
        
        return weighted_embedding
    except Exception as e:
        logger.error(f"Error computing weighted embedding for user {user_id}: {e}")
        raise

def recommend_for_user(user_id: str, top_k: int = 5):
    try:
        user_embedding = compute_weighted_embedding(user_id)
        
        recommendations = client.search(
            collection_name="product",
            query_vector=user_embedding,
            limit=top_k
        )
        recommended_product_ids = [rec.payload["product_id"] for rec in recommendations]

        update_recommendations_in_postgres(user_id, recommended_product_ids)
        
        logger.info(f"🟢 Recommendations for user {user_id}: {recommended_product_ids}")
        sys.stdout.flush()
        return recommended_product_ids
    except Exception as e:
        logger.error(f"Error generating recommendations for user {user_id}: {e}")
        raise

def process_kafka_message(message):
    try:
        # Parse the message (assuming it is JSON-encoded)
        document = json.loads(message.value.decode('utf-8'))
        
        # Optionally, trigger recommendations or further processing based on the message
        after_data = eval(document.get("payload").get("after"))
        logger.info(f'🟢 after_data')
        pprint(after_data)
        user_id = after_data.get("user_id")
        logger.info(f'🟢 {user_id=}')
        if user_id:
            recommendations = recommend_for_user(user_id, 20)
            logger.info(f"⚙️ Processed message for user {user_id} with recommendations: {recommendations}")
            sys.stdout.flush()
    except Exception as e:
        logger.error(f"Error processing Kafka message: {e}")

def consume_kafka_messages():
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=f"{KAFKA_HOST}:{KAFKA_PORT}",
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id='recommendation-group'
        )

        logger.info("✈️ Kafka consumer started. Waiting for messages...")
        sys.stdout.flush()
        for message in consumer:
            # logger.info(f"⚙️ Received message: {message.value.decode('utf-8')}")
            sys.stdout.flush()
            process_kafka_message(message)
    except Exception as e:
        logger.error(f"Error in Kafka consumer: {e}")

if __name__ == "__main__":
    consume_kafka_messages()