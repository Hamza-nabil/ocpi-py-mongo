from ocpi.modules.versions.enums import VersionNumber

from ocpi.modules.cdrs.v_2_2_1.schemas import Cdr
from ocpi.modules.credentials.v_2_2_1.schemas import Credentials
from ocpi.modules.locations.v_2_2_1.schemas import Location
from ocpi.modules.sessions.v_2_2_1.schemas import Session
from ocpi.modules.tariffs.v_2_2_1.schemas import Tariff
from ocpi.modules.tokens.v_2_2_1.schemas import Token


class Adapter:
    @classmethod
    def location_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI Location schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional): The version number of the caller OCPI module

        Returns:
            Location: The object data in proper OCPI schema
        """
        return Location(**data)

    @classmethod
    def session_adapter(cls, data: dict, version: VersionNumber = VersionNumber.latest):
        """Adapt the data to OCPI Session schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional): The version number of the caller OCPI module

        Returns:
            Session: The object data in proper OCPI schema
        """
        return Session(**data)

    @classmethod
    def charging_preference_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI ChargingPreference schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional): The version number of the caller OCPI module

        Returns:
            ChargingPreference: The object data in proper OCPI schema
        """
        #return ChargingPreference(**data)

    @classmethod
    def credentials_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI Credential schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional): The version number of the caller OCPI module

        Returns:
            Credential: The object data in proper OCPI schema
        """
        return Credentials(**data)

    @classmethod
    def cdr_adapter(cls, data: dict, version: VersionNumber = VersionNumber.latest):
        """Adapt the data to OCPI CDR schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional): The version number of the caller OCPI module

        Returns:
            CDR: The object data in proper OCPI schema
        """
        return Cdr(**data)

    @classmethod
    def tariff_adapter(cls, data: dict, version: VersionNumber = VersionNumber.latest):
        """Adapt the data to OCPI Tariff schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional): The version number of the caller OCPI module

        Returns:
            Tariff: The object data in proper OCPI schema
        """
        return Tariff(**data)

    @classmethod
    def command_response_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI CommandResponse schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional): The version number of the caller OCPI module

        Returns:
            CommandResponse: The object data in proper OCPI schema
        """

    @classmethod
    def command_result_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI CommandResult schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional): The version number of the caller OCPI module

        Returns:
            CommandResult: The object data in proper OCPI schema
        """

    @classmethod
    def token_adapter(cls, data: dict, version: VersionNumber = VersionNumber.latest):
        """Adapt the data to OCPI Token schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional): The version number of the caller OCPI module

        Returns:
            Token: The object data in proper OCPI schema
        """
        return Token(**data)

    @classmethod
    def authorization_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI AuthorizationInfo schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional): The version number of the caller OCPI module

        Returns:
            AuthorizationInfo: The object data in proper OCPI schema
        """
