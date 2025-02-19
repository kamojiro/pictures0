import os

import google.auth
from google.auth import impersonated_credentials
from google.cloud import storage
from google.oauth2.service_account import Credentials

from utils.metadata import get_metadata


def get_storage_client():
    if os.environ.get("K_SERVICE"):
        credentials, project = google.auth.default()
        service_account_email = get_metadata("email")
        signing_credentials = impersonated_credentials.Credentials(
            source_credentials=credentials,
            target_principal=service_account_email,
            # target_scopes="https://www.googleapis.com/auth/devstorage.read_write",
            target_scopes="https://www.googleapis.com/auth/devstorage.full_control",
            lifetime=10,
        )
        return storage.Client(credentials=signing_credentials)
    else:
        service_account_key_path = "../.credential/service_account_key.json"
        credentials = Credentials.from_service_account_file(
            filename=service_account_key_path
        )
        return storage.Client(credentials=credentials)
