from fastapi import APIRouter, Depends, Request

from ocpi.core.dependencies import get_crud, get_adapter
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.core.schemas import OCPIResponse
from ocpi.core.adapter import Adapter
from ocpi.core.crud import Crud
from ocpi.core import status
from ocpi.core.utils import get_auth_token
from ocpi.modules.versions.enums import VersionNumber
from ocpi.modules.commands.v_2_2_1.schemas import CommandResult

router = APIRouter(
    prefix='/commands',
)


@router.post("/{uid}", response_model=OCPIResponse)
async def receive_command_result(request: Request, uid: str, command_result: CommandResult,
                                 crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)

    await crud.update(ModuleID.commands, RoleEnum.emsp, command_result.dict(), uid,
                      auth_token=auth_token, version=VersionNumber.v_2_2_1)

    return OCPIResponse(
        data=[],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
