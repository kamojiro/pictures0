from fastapi import APIRouter, Depends, HTTPException, Query

from services.gcs_service import GCSService

router = APIRouter(prefix="/gcs", tags=["gcs"])


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
        url, title, tags = gcs_service.get_random_signed_url("ocmai", expiration)
        return {"signed_url": url, "title": title, "tags": tags}
    except Exception as e:
        return HTTPException(
            status_code=500, detail=f"Failed to generate signed URL: {e}"
        )
