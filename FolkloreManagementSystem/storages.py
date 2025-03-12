import os
from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    """Azure Storage class for media files."""
    account_name = "instrumentstorage"  # Your Azure Storage Account name
    account_key = os.getenv("AZURE_ACCOUNT_KEY")  # Get key securely from environment
    azure_container = "instrument-photos"
    expiration_secs = None  # Publicly accessible images

    if not account_key:
        raise ValueError("Missing AZURE_ACCOUNT_KEY environment variable")
