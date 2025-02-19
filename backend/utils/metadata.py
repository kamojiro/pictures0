import os
from functools import lru_cache
from typing import Literal

import requests


@lru_cache
def get_metadata(metadatakey: Literal["email", "project-id"]) -> str:
    print(f"🔷{os.environ.get('K_SERVICE')}=")
    if os.environ.get("K_SERVICE") is not None:
        metadata_url = f"http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/{metadatakey}"
        headers = {"Metadata-Flavor": "Google"}
        try:
            response = requests.get(metadata_url, headers=headers, timeout=2)
            response.raise_for_status()
            return response.text.strip()
        except Exception as e:
            raise RuntimeError(
                f"Failed to get service account {metadatakey} from metadata server.\n failed to access {metadata_url}"
            ) from e
    else:
        metadata = os.environ.get(metadatakey.upper().replace("-", "_"))
        if metadata is None:
            raise RuntimeError(f"Failed to get {metadatakey} from environment variable")
        return metadata
