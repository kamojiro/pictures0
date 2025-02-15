from google.cloud import storage
from google.oauth2.service_account import Credentials


import os


def get_storage_client():
    if os.environ.get("K_SERVICE"):
        return storage.Client()
    else:
        print(f"♢{os.getcwd()=}")
        service_account_key_path = "../.credential/service_account_key.json"
        credentials = Credentials.from_service_account_file(
            filename=service_account_key_path
        )
        return storage.Client(credentials=credentials)
