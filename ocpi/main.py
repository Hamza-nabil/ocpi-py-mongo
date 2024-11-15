from typing import Any, List
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from ocpi.core.endpoints import ENDPOINTS

from ocpi.modules.versions.api import router as versions_router, versions_v_2_2_1_router
from ocpi.modules.versions.enums import VersionNumber
from ocpi.modules.versions.schemas import Version
from ocpi.core.dependencies import get_versions, get_endpoints
from ocpi.core import status
from ocpi.core.enums import RoleEnum
from ocpi.core.config import settings
from ocpi.core.data_types import URL
from ocpi.core.schemas import OCPIResponse
from ocpi.core.exceptions import AuthorizationOCPIError, NotFoundOCPIError
from ocpi.core.push import (
    http_router as http_push_router,
    websocket_router as websocket_push_router,
)
from ocpi.routers import v_2_2_1_cpo_router, v_2_2_1_emsp_router
from ocpi.core.db import get_db, ping, client_close


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            response = await call_next(request)
        except AuthorizationOCPIError as e:
            raise HTTPException(403, str(e)) from e
        except NotFoundOCPIError as e:
            raise HTTPException(404, str(e)) from e
        except ValidationError:
            response = JSONResponse(
                OCPIResponse(
                    data=[],
                    **status.OCPI_3000_GENERIC_SERVER_ERROR,
                ).dict()
            )
        return response


@asynccontextmanager
async def db_lifespan(app: FastAPI):
    # Startup
    app.database = get_db()
    ping_response = await ping()
    # if int(ping_response["ok"]) != 1:
    #     raise Exception("Problem connecting to database cluster.")
    # else:
    #     logging.info("Connected to database cluster.")

    yield

    # Shutdown
    client_close()


def get_application(
    version_numbers: List[VersionNumber],
    roles: List[RoleEnum],
    http_push: bool = False,
    websocket_push: bool = False,
) -> FastAPI:
    _app = FastAPI(
        lifespan=db_lifespan,
        title=settings.PROJECT_NAME,
        docs_url=f"/{settings.OCPI_PREFIX}/docs",
        openapi_url=f"/{settings.OCPI_PREFIX}/openapi.json",
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.add_middleware(ExceptionHandlerMiddleware)

    _app.include_router(
        versions_router,
        prefix=f"/{settings.OCPI_PREFIX}",
    )

    if http_push:
        _app.include_router(
            http_push_router,
            prefix=f"/{settings.PUSH_PREFIX}",
        )

    if websocket_push:
        _app.include_router(
            websocket_push_router,
            prefix=f"/{settings.PUSH_PREFIX}",
        )

    versions = []
    version_endpoints = {}

    if VersionNumber.v_2_2_1 in version_numbers:
        _app.include_router(
            versions_v_2_2_1_router,
            prefix=f"/{settings.OCPI_PREFIX}",
        )

        versions.append(
            Version(
                version=VersionNumber.v_2_2_1,
                url=URL(
                    f"https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/{VersionNumber.v_2_2_1.value}/details"
                ),
            ).dict(),
        )

        version_endpoints[VersionNumber.v_2_2_1] = []

        if RoleEnum.cpo in roles:
            _app.include_router(
                v_2_2_1_cpo_router,
                prefix=f"/{settings.OCPI_PREFIX}/cpo/{VersionNumber.v_2_2_1.value}",
                tags=["CPO"],
            )
            version_endpoints[VersionNumber.v_2_2_1] += ENDPOINTS[
                VersionNumber.v_2_2_1
            ][RoleEnum.cpo]

        if RoleEnum.emsp in roles:
            _app.include_router(
                v_2_2_1_emsp_router,
                prefix=f"/{settings.OCPI_PREFIX}/emsp/{VersionNumber.v_2_2_1.value}",
                tags=["EMSP"],
            )
            version_endpoints[VersionNumber.v_2_2_1] += ENDPOINTS[
                VersionNumber.v_2_2_1
            ][RoleEnum.emsp]

    def override_get_versions():
        return versions

    _app.dependency_overrides[get_versions] = override_get_versions

    def override_get_endpoints():
        return version_endpoints

    _app.dependency_overrides[get_endpoints] = override_get_endpoints

    return _app


app = get_application([VersionNumber.v_2_2_1], settings.ROLES)
