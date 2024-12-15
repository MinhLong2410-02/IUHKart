import os
ENABLE_PROXY_FIX = True

SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set")

SQLALCHEMY_DATABASE_URI = os.getenv("SUPERSET_DATABASE_URI") + "?options=-csearch_path=superset"
SQLALCHEMY_SCHEMA = "superset"

PREVENT_UNSAFE_DB_CONNECTIONS = False


TALISMAN_ENABLED = False
WTF_CSRF_ENABLED = False


PUBLIC_ROLE_LIKE = "Gamma"
DEBUG = True


#EMBED
FEATURE_FLAGS = {
    "EMBEDDED_SUPERSET": True, # Embed dashboards
    "EMBEDDABLE_CHARTS": True # Embed individual chart
}

# CORS
ENABLE_CORS = True  
CORS_OPTIONS = { 
    "supports_credentials": True, 
    "allow_headers": "*", 
    "expose_headers": "*", 
    "resources": "*", 
    "origins": ["http://localhost:4200","http://localhost:3000", "*"] #4200 for angular , 3000 for react  
}

# Dashboard embedding 
GUEST_ROLE_NAME = "Gamma" 
GUEST_TOKEN_JWT_SECRET = SECRET_KEY
GUEST_TOKEN_JWT_ALGO = "HS256" 
GUEST_TOKEN_HEADER_NAME = "X-GuestToken" 
GUEST_TOKEN_JWT_EXP_SECONDS = 300 # 5 minutes