from fastapi import APIRouter, Depends, HTTPException, Query
from services.gcs_service import GCSService

router = APIRouter(prefix="/gcs", tags=["gcs"])


@router.get("/random/ocmai/signed-url")
async def get_signed_url(
    expiration: int = Query(15, description="署名付き URL の有効期限（分）"),
    gcs_service: GCSService = Depends(GCSService),
):
    try:
        url = gcs_service.get_random_signed_url("ocmai", expiration)
        return {"signed_url": url}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate signed URL: {e}"
        )
