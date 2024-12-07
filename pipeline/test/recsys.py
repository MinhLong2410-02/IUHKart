

BEHAVIOR_WEIGHTS = {
    "search": 1,
    "view": 3,
    "add_to_cart": 5,
    "purchase": 10
}
def get_user_behavior_weights(user_id: str):
    # Query behaviors for the user
    user_behaviors = db.behaviors.find({"user_id": user_id})
    
    # Aggregate weights by product_id
    product_weights = {}
    for behavior in user_behaviors:
        product_id = behavior["product_id"]
        weight = behavior["weight"]
        product_weights[product_id] = product_weights.get(product_id, 0) + weight
    
    return product_weights