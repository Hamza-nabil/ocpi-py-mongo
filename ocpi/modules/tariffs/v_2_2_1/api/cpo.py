from fastapi import APIRouter, Depends, Response, Request

from ocpi.core.utils import get_list, get_auth_token
from ocpi.core import status
from ocpi.core.schemas import OCPIResponse
from ocpi.core.adapter import Adapter
from ocpi.core.crud import Crud
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.core.dependencies import get_crud, get_adapter, pagination_filters
from ocpi.modules.versions.enums import VersionNumber

router = APIRouter(
    prefix='/tariffs',
)


@router.get("/", response_model=OCPIResponse)
async def get_tariffs(request: Request,
                      response: Response,
                      crud: Crud = Depends(get_crud),
                      adapter: Adapter = Depends(get_adapter),
                      filters: dict = Depends(pagination_filters)):
    auth_token = get_auth_token(request)

    data_list = await get_list(response, filters, ModuleID.tariffs, RoleEnum.cpo,
                               VersionNumber.v_2_2_1, crud, auth_token=auth_token)

    tariffs = []
    for data in data_list:
        tariffs.append(adapter.tariff_adapter(data).dict())
    return OCPIResponse(
        data=tariffs,
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
