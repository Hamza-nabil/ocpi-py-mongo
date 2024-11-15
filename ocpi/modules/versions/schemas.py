from typing import List

from pydantic import BaseModel

from ocpi.modules.versions.enums import VersionNumber, InterfaceRole
from ocpi.core.data_types import URL
from ocpi.core.enums import ModuleID


class Version(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/version_information_endpoint.asciidoc#121-data
    """

    version: VersionNumber
    url: URL


class Endpoint(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/version_information_endpoint.asciidoc#122-endpoint-class
    """

    identifier: ModuleID
    role: InterfaceRole
    url: URL


class VersionDetail(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/version_information_endpoint.asciidoc#121-data
    """

    version: VersionNumber
    endpoints: List[Endpoint]
