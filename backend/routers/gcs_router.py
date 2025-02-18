from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from services.gcs_service import GCSService

router = APIRouter(prefix="/gcs", tags=["gcs"])

BUCKET_NAME = "ocmai"


@router.get("/ocmai/list")
async def list_buckets(gcs_service: GCSService = Depends(GCSService)):
    try:
        return {"ocmai": [blob.metadata["title"] for blob in gcs_service.list()]}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Failed to list buckets: {e}")


@router.get("/ocmai/random/signed-url")
async def get_signed_url(
    expiration: int = Query(15, description="署名付き URL の有効期限(分)"),
    gcs_service: GCSService = Depends(GCSService),
):
    try:
        url, title, tags = gcs_service.get_random_signed_url(BUCKET_NAME, expiration)
        return {"signed_url": url, "title": title, "tags": tags}
    except Exception as e:
        return HTTPException(
            status_code=500, detail=f"Failed to generate signed URL: {e}"
        )


@router.post("/ocmai/upload")
async def upload_file(
    # background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    gcs_service: GCSService = Depends(GCSService),
):
    """Receives a PDF file, registers it in the database, saves it to storage,
    and triggers asynchronous processing.
    """
    filename = file.filename
    content_type = file.content_type
    # file.file.seek(0)
    blob_name = gcs_service.upload(BUCKET_NAME, filename, file.file, content_type)
    metadata = gcs_service.add_metadata(BUCKET_NAME, blob_name, content_type)
    return {"blob_name": blob_name, "metadata": metadata}
