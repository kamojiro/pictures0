import datetime
import random

from utils.gcs_client import get_storage_client

SAMPLES = [
    "gs://ocmai/any/kamomo_heart.png",
    "gs://ocmai/any/kamomo_conveyor_belt.webp",
    "gs://ocmai/any/fes_kamomo_amomo.webp",
    "gs://ocmai/any/amomo_jitensha.webp",
]


def get_blob_name(bucket_name: str, blob_name: str) -> str:
    return blob_name.split(f"/{bucket_name}/", 1)[1]


class GCSService:
    def __init__(self):
        self.client = get_storage_client()

    def list(self, bucket_name: str = "ocmai"):
        bucket = self.client.bucket(bucket_name)
        blobs = bucket.list_blobs(
            prefix="any/", delimiter="/", include_folders_as_prefixes=False
        )
        return [blob for blob in blobs if not blob.name.endswith("/")]

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

    def get_random_signed_url(
        self, bucket_name="ocmai", expiration_minutes: int = 15
    ) -> tuple:
        blobs = self.list(bucket_name)
        blob_name_list = [f"gs://{blob.bucket.name}/{blob.name}" for blob in blobs]
        random_index = random.randint(0, len(blobs))  # noqa: S311
        return (
            self._generate_signed_url(bucket_name, blob_name_list[random_index]),
            blobs[random_index].metadata["title"],
            blobs[random_index].metadata["tags"],
        )
