from storages.backends.azure_storage import AzureStorage
from os import environ
from dotenv import load_dotenv
load_dotenv('./.env')
# Azure Blob Storage settings
AZURE_CONNECTION_STRING = environ.get('AZURE_CONNECTION_STRING')

class AzureCustomStorage(AzureStorage):
    account_name = environ.get('AZURE_ACCOUNT_NAME')
    account_key = environ.get('AZURE_ACCOUNT_KEY')
    expiration_secs = None
    
class AzureCustomerStorage(AzureCustomStorage):
    azure_container = 'customer'  

class AzureVendorStorage(AzureCustomStorage):
    azure_container = 'vendor'  