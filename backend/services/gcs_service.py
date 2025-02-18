import datetime
import json
import random

import vertexai
from fastapi import File
from vertexai.generative_models import GenerationConfig, GenerativeModel, Part

from utils.gcs_client import get_storage_client
from utils.metadata import get_metadata

SAMPLES = [
    "gs://ocmai/any/kamomo_heart.png",
    "gs://ocmai/any/kamomo_conveyor_belt.webp",
    "gs://ocmai/any/fes_kamomo_amomo.webp",
    "gs://ocmai/any/amomo_jitensha.webp",
]

# TODO: データは取得する
SAMPLES_JSON = [
    {"title": "かももハート", "tags": "かもも"},
    {"title": "かももベルトコンベア", "tags": "かもも,おしまい"},
    {"title": "かももあももフェス", "tags": "かもも,あもも"},
    {"title": "あもも自転車", "tags": "あもも"},
]

EXAMPLE_PROMPT = []
for i in range(4):
    EXAMPLE_PROMPT.append("INPUT:")
    EXAMPLE_PROMPT.append(Part.from_uri(SAMPLES[i], mime_type="image/webp"))
    EXAMPLE_PROMPT.append("OUTPUT:")
    EXAMPLE_PROMPT.append(json.dumps(SAMPLES_JSON[i], ensure_ascii=False, indent=2))

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "tags": {"type": "string"},
    },
    "required": ["title", "tags"],
}

PROMPT = """
画像を分析して、タイトルとタグをつけてください。日本語で回答してください。
タイトルは、キャラクター名と場面を表す名前にしてください。
タグは、キャラクター名と関連するものを含めてください。
キャラクター名は、かもも、あもも、おしまい、その他のいずれかです。
- かもも: 緑色の頭と茶色の胴体を持つ、ずんぐりした体型の鴨のキャラクター
- あもも: 色いふわふわした体に、頭に炎を持つ、からあげのキャラクター
- おしまい: ピンクの髪を丸い飾りのついたおさげ髪の女の子のキャラクター
- その他: かもも、あもも、おしまい以外のキャラクター
"""


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

    def generate_metadata(self, bucket_name: str, blob_name: str, content_type: str):
        vertexai.init(project=get_metadata("project-id"), location="us-central1")
        model = GenerativeModel("gemini-2.0-flash-001")
        gcs_path = f"gs://{bucket_name}/{blob_name}"
        response = model.generate_content(
            [
                PROMPT,
                "<EXAMPLES>",
                *EXAMPLE_PROMPT,
                "</EXAMPLES>",
                "INPUT:",
                Part.from_uri(
                    gcs_path,
                    mime_type=content_type,
                ),
                "OUTPUT:",
            ],
            generation_config=GenerationConfig(
                response_mime_type="application/json", response_schema=RESPONSE_SCHEMA
            ),
        )
        metadata = json.loads(response.text)
        return metadata

    def add_metadata(self, bucket_name: str, blob_name: str, content_type: str | None):
        if content_type is None:
            raise ValueError("Content-Type is required")
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.metadata = self.generate_metadata(bucket_name, blob_name, content_type)
        blob.patch()
        return blob.metadata

    def upload(
        self, bucket_name: str, filename: str | None, file_obj, content_type: str | None
    ):
        if not filename:
            raise ValueError("Filename is required")
        if not content_type:
            raise ValueError("Content-Type is required")
        blob_name = f"any/{filename}"
        bucket = self.client.bucket(bucket_name)
        existing_blob = bucket.get_blob(blob_name)
        if existing_blob:
            raise FileExistsError(f"File already exists: {blob_name}")
        blob = bucket.blob(blob_name)
        blob.upload_from_file(file_obj, content_type=content_type)
        return blob.name

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
