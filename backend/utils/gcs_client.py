import requests
from functools import lru_cache

from google.cloud import storage
from google.auth import impersonated_credentials
from google.oauth2.service_account import Credentials
import google.auth

import os


@lru_cache
def get_service_account_email() -> str:
    metadata_url = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/email"
    headers = {"Metadata-Flavor": "Google"}
    try:
        response = requests.get(metadata_url, headers=headers, timeout=2)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        raise RuntimeError(
            "Failed to get service account email from metadata server"
        ) from e


def get_storage_client():
    if os.environ.get("K_SERVICE"):
        credentials, project = google.auth.default()
        service_account_email = get_service_account_email()
        signing_credentials = impersonated_credentials.Credentials(
            source_credentials=credentials,
            target_principal=service_account_email,
            target_scopes="https://www.googleapis.com/auth/devstorage.read_write",
            lifetime=10,
        )
        return storage.Client(credentials=signing_credentials)
    else:
        service_account_key_path = "../.credential/service_account_key.json"
        credentials = Credentials.from_service_account_file(
            filename=service_account_key_path
        )
        return storage.Client(credentials=credentials)
