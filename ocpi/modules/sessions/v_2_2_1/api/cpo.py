from fastapi import APIRouter, Depends, Response, Request

from ocpi.modules.sessions.v_2_2_1.schemas import ChargingPreferences
from ocpi.modules.versions.enums import VersionNumber
from ocpi.core.utils import get_list, get_auth_token
from ocpi.core import status
from ocpi.core.schemas import OCPIResponse
from ocpi.core.adapter import Adapter
from ocpi.core.crud import Crud
from ocpi.core.data_types import CiString
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.core.dependencies import get_crud, get_adapter, pagination_filters

router = APIRouter(
    prefix="/sessions",
)


@router.get("/", response_model=OCPIResponse)
async def get_sessions(
    request: Request,
    response: Response,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
    filters: dict = Depends(pagination_filters),
):
    auth_token = get_auth_token(request)

    data_list = await get_list(
        response,
        filters,
        ModuleID.sessions,
        RoleEnum.cpo,
        VersionNumber.v_2_2_1,
        crud,
        auth_token=auth_token,
    )

    sessions = []
    for data in data_list:
        sessions.append(adapter.session_adapter(data).dict())
    return OCPIResponse(
        data=sessions,
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.put("/{session_id}/charging_preferences", response_model=OCPIResponse)
async def set_charging_preference(
    request: Request,
    session_id: CiString(36),
    charging_preferences: ChargingPreferences,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    auth_token = get_auth_token(request)
    data = await crud.update(
        ModuleID.sessions,
        RoleEnum.cpo,
        charging_preferences.dict(),
        session_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_2_1,
    )
    return OCPIResponse(
        data=[adapter.charging_preference_adapter(data).dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
