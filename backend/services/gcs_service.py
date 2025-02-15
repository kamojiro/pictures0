import os
import datetime
import random

from google.cloud import storage
from utils.gcs_client import get_storage_client

def get_blob_name(bucket_name: str, blob_name: str) -> str:
    return blob_name.split(f"/{bucket_name}/", 1)[1]


class GCSService:
    def __init__(self):
        self.client = get_storage_client()

    def _generate_signed_url(
        self, bucket_name: str, blob_name: str, expiration_minutes: int = 15
    ) -> str:
        """
        指定した GCS バケット内のオブジェクトに対する署名付き URL を生成します。

        :param bucket_name: バケット名
        :param blob_name: 署名付き URL を発行する対象のオブジェクト名（キー）
        :param expiration_minutes: URL の有効期限（分単位、デフォルトは 15 分）
        :return: 署名付き URL（GET リクエスト用）
        """
        bucket = self.client.bucket(bucket_name)
        print(f"{get_blob_name(bucket_name, blob_name)=}")
        blob = bucket.blob(get_blob_name(bucket_name, blob_name))
        # V4署名付きURLを生成
        url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(minutes=expiration_minutes),
            method="GET",
        )
        print(f"{url=}")
        return url

    def get_random_signed_url(self, bucket_name="ocmai",expiration_minutes: int = 15) -> str:
        blob_name_list = [
            "gs://ocmai/kamomo/4530ea9ccf6c6cf7.webp",
            "gs://ocmai/kamomo/fcdf2191d04dee4f.webp",
            "gs://ocmai/kamomo/kamomo_photobomb.webp",
            "gs://ocmai/amomo/41c2587fd9e225a7.webp",
        ]
        random_index = random.randint(0, 3)
        return self._generate_signed_url(bucket_name, blob_name_list[random_index])
