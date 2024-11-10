from typing import Any, Tuple

from ocpi.core.db import get_db
from motor.core import AgnosticDatabase
from ocpi.core.enums import ModuleID, RoleEnum, Action


class Crud:
    _database: AgnosticDatabase = get_db()

    @classmethod
    async def get(cls, module: ModuleID, role: RoleEnum, id, *args, **kwargs) -> Any:
        """Get an object

        Args:
            module (ModuleID): The OCPI module
            role (RoleEnum): The role of the caller
            id (Any): The ID of the object

        Keyword Args:
            auth_token (str): The authentication token used by third party
            version (VersionNumber): The version number of the caller OCPI module
            party_id (CiString(3)):  The requested party ID
            country_code (CiString(2)): The requested Country code
            token_type (TokenType): The token type
            command (CommandType): The command type of the OCPP command

        Returns:
            Any: The object data
        """
        collection = cls._database[module.value]
        document = await collection.find_one({"_id": id})
        return document

    @classmethod
    async def list(
        cls, module: ModuleID, role: RoleEnum, filters: dict, *args, **kwargs
    ) -> Tuple[list, int, bool]:
        """Get the list of objects

        Args:
            module (ModuleID): The OCPI module
            role (RoleEnum): The role of the caller
            filters (dict): OCPI pagination filters

        Keyword Args:
            auth_token (str): The authentication token used by third party
            version (VersionNumber): The version number of the caller OCPI module
            party_id (CiString(3)): The requested party ID
            country_code (CiString(2)): The requested Country code

        Returns:
            Tuple[list, int, bool]: Objects list, Total number of objects, if it's the last page or not(for pagination)
        """
        collection = cls._database[module.value]
        cursor = collection.find(filters)

        # Apply pagination if needed
        limit = kwargs.get("limit", 10)
        skip = kwargs.get("skip", 0)
        cursor = cursor.skip(skip).limit(limit)

        documents = await cursor.to_list(length=limit)
        total_count = await collection.count_documents(filters)
        is_last_page = (skip + limit) >= total_count

        return documents, total_count, is_last_page

    @classmethod
    async def create(
        cls, module: ModuleID, role: RoleEnum, data: dict, *args, **kwargs
    ) -> Any:
        """Create an object

        Args:
            module (ModuleID): The OCPI module
            role (RoleEnum): The role of the caller
            data (dict): The object details

        Keyword Args:
            auth_token (str): The authentication token used by third party
            version (VersionNumber): The version number of the caller OCPI module
            command (CommandType): The command type (used in Commands module)
            party_id (CiString(3)):  The requested party ID
            country_code (CiString(2)): The requested Country code
            token_type (TokenType): The token type
            operation ('credentials', 'registration'): The operation type in credentials and registration process

        Returns:
            Any: The created object data
        """
        collection = cls._database[module.value]
        result = await collection.insert_one(data)
        created_document = await collection.find_one({"_id": result.inserted_id})
        return created_document

    @classmethod
    async def update(
        cls, module: ModuleID, role: RoleEnum, data: dict, id, *args, **kwargs
    ) -> Any:
        """Update an object

        Args:
            module (ModuleID): The OCPI module
            role (RoleEnum): The role of the caller
            data (dict): The object details
            id (Any): The ID of the object

        Keyword Args:
            auth_token (str): The authentication token used by third party
            version (VersionNumber): The version number of the caller OCPI module
            party_id (CiString(3)):  The requested party ID
            country_code (CiString(2)): The requested Country code
            token_type (TokenType): The token type
            operation ('credentials', 'registration'): The operation type in credentials and registration process


        Returns:
            Any: The updated object data
        """
        collection = cls._database[module.value]
        result = await collection.insert_one(data)
        created_document = await collection.find_one({"_id": result.inserted_id})
        return created_document

    @classmethod
    async def delete(cls, module: ModuleID, role: RoleEnum, id, *args, **kwargs):
        """Delete an object

        Args:
            module (ModuleID): The OCPI module
            role (RoleEnum): The role of the caller
            id (Any): The ID of the object

        Keyword Args:
            auth_token (str): The authentication token used by third party
            version (VersionNumber): The version number of the caller OCPI module
        """
        collection = cls._database[module.value]
        result = await collection.delete_one({"_id": id})
        return result.deleted_count > 0  # Returns True if a document was deleted

    @classmethod
    async def do(
        cls,
        module: ModuleID,
        role: RoleEnum,
        action: Action,
        *args,
        data: dict = None,
        **kwargs
    ) -> Any:
        """Do an action (non-CRUD)

        Args:
            module (ModuleID): The OCPI module
            role (RoleEnum): The role of the caller
            action (Action): The action type
            data (dict): The data required for the action
            command (CommandType): The command type of the OCPP command

        Keyword Args:
            auth_token (str): The authentication token used by third party
            version (VersionNumber): The version number of the caller OCPI module

        Returns:
            Any: The action result
        """
        pass
