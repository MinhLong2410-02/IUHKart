import os, requests

TRACKING_API_URL = os.getenv('TRACKING_API')
tracking_session = requests.Session()

def search_tracking(product_ids: list, access_token: str):
    """
    Sends product IDs and access token to the tracking API and returns the results.

    Args:
        product_ids (list): List of product IDs to track.
        access_token (str): Access token for authentication.

    Returns:
        dict: JSON response from the tracking API.
    """
    if not TRACKING_API_URL:
        raise ValueError("TRACKING_API_URL is not set in the environment variables.")
    
    headers = {"Authorization": f"Bearer {access_token}"}  
    payload = {"event_type": "search", "product_ids": product_ids}
    response = tracking_session.post(TRACKING_API_URL, json=payload, headers=headers, timeout=10)
    response.raise_for_status() 
    # try:
    #     response = tracking_session.post(TRACKING_API_URL, json=payload, headers=headers, timeout=10)
    #     response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)

    #     # Parse and return the response JSON
    #     return response.json().get('results', {})
    # except requests.exceptions.RequestException as e:
    #     raise RuntimeError(f"Error while calling tracking API: {e}") from e