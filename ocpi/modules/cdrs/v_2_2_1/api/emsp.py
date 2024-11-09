from fastapi import APIRouter, Depends, Request, Response

from ocpi.modules.cdrs.v_2_2_1.schemas import Cdr
from ocpi.modules.versions.enums import VersionNumber
from ocpi.core.utils import get_auth_token
from ocpi.core import status
from ocpi.core.schemas import OCPIResponse
from ocpi.core.adapter import Adapter
from ocpi.core.crud import Crud
from ocpi.core.data_types import CiString
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.core.config import settings
from ocpi.core.dependencies import get_crud, get_adapter

router = APIRouter(
    prefix='/cdrs',
)


@router.get("/{cdr_id}", response_model=OCPIResponse)
async def get_cdr(request: Request, cdr_id: CiString(36),
                  crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)

    data = await crud.get(ModuleID.cdrs, RoleEnum.emsp, cdr_id, auth_token=auth_token,
                          version=VersionNumber.v_2_2_1)
    return OCPIResponse(
        data=[adapter.cdr_adapter(data, VersionNumber.v_2_2_1).dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.post("/", response_model=OCPIResponse)
async def add_cdr(request: Request, response: Response, cdr: Cdr,
                  crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)

    data = await crud.create(ModuleID.cdrs, RoleEnum.emsp, cdr.dict(),
                             auth_token=auth_token, version=VersionNumber.v_2_2_1)

    cdr_data = adapter.cdr_adapter(data)
    cdr_url = (f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp'
               f'/{VersionNumber.v_2_2_1}/{ModuleID.cdrs}/{cdr_data.id}')
    response.headers.append('Location', cdr_url)

    return OCPIResponse(
        data=[cdr_data.dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
