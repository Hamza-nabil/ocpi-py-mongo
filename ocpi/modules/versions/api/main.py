from fastapi import APIRouter, Depends

from ocpi.core import status
from ocpi.core.dependencies import get_versions as get_versions_
from ocpi.core.schemas import OCPIResponse

router = APIRouter()


@router.get("/versions", response_model=OCPIResponse)
async def get_versions(versions=Depends(get_versions_)):
    return OCPIResponse(
        data=versions,
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
