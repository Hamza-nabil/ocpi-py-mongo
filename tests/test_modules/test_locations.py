from uuid import uuid4

from fastapi.testclient import TestClient

from ocpi.main import get_application
from ocpi.core import enums
from ocpi.core.config import settings
from ocpi.modules.locations.v_2_2_1.schemas import Location
from ocpi.modules.versions.enums import VersionNumber


LOCATIONS = [
    {
        "country_code": "us",
        "party_id": "AAA",
        "id": str(uuid4()),
        "publish": True,
        "publish_allowed_to": [
            {
                "uid": str(uuid4()),
                "type": "APP_USER",
                "visual_number": "1",
                "issuer": "issuer",
                "group_id": "group_id",
            },
        ],
        "name": "name",
        "address": "address",
        "city": "city",
        "postal_code": "111111",
        "state": "state",
        "country": "USA",
        "coordinates": {
            "latitude": "latitude",
            "longitude": "longitude",
        },
        "related_locations": [
            {
                "latitude": "latitude",
                "longitude": "longitude",
                "name": {"language": "en", "text": "name"},
            },
        ],
        "parking_type": "ON_STREET",
        "evses": [
            {
                "uid": str(uuid4()),
                "evse_id": str(uuid4()),
                "status": "AVAILABLE",
                "status_schedule": {
                    "period_begin": "2022-01-01T00:00:00+00:00",
                    "period_end": "2022-01-01T00:00:00+00:00",
                    "status": "AVAILABLE",
                },
                "capabilities": [
                    "CREDIT_CARD_PAYABLE",
                ],
                "connectors": [
                    {
                        "id": str(uuid4()),
                        "standard": "DOMESTIC_A",
                        "format": "SOCKET",
                        "power_type": "DC",
                        "max_voltage": 100,
                        "max_amperage": 100,
                        "max_electric_power": 100,
                        "tariff_ids": [
                            str(uuid4()),
                        ],
                        "terms_and_conditions": "https://www.example.com",
                        "last_updated": "2022-01-01T00:00:00+00:00",
                    }
                ],
                "floor_level": "3",
                "coordinates": {
                    "latitude": "latitude",
                    "longitude": "longitude",
                },
                "physical_reference": "pr",
                "directions": [
                    {"language": "en", "text": "directions"},
                ],
                "parking_restrictions": [
                    "EV_ONLY",
                ],
                "images": [
                    {
                        "url": "https://www.example.com",
                        "thumbnail": "https://www.example.com",
                        "category": "CHARGER",
                        "type": "type",
                        "width": 10,
                        "height": 10,
                    },
                ],
                "last_updated": "2022-01-01T00:00:00+00:00",
            }
        ],
        "directions": [
            {"language": "en", "text": "directions"},
        ],
        "operator": {
            "name": "name",
            "website": "https://www.example.com",
            "logo": {
                "url": "https://www.example.com",
                "thumbnail": "https://www.example.com",
                "category": "CHARGER",
                "type": "type",
                "width": 10,
                "height": 10,
            },
        },
        "suboperator": {
            "name": "name",
            "website": "https://www.example.com",
            "logo": {
                "url": "https://www.example.com",
                "thumbnail": "https://www.example.com",
                "category": "CHARGER",
                "type": "type",
                "width": 10,
                "height": 10,
            },
        },
        "owner": {
            "name": "name",
            "website": "https://www.example.com",
            "logo": {
                "url": "https://www.example.com",
                "thumbnail": "https://www.example.com",
                "category": "CHARGER",
                "type": "type",
                "width": 10,
                "height": 10,
            },
        },
        "facilities": ["MALL"],
        "time_zone": "UTC+2",
        "opening_times": {
            "twentyfourseven": True,
            "regular_hours": [
                {
                    "weekday": 1,
                    "period_begin": "8:00",
                    "period_end": "22:00",
                },
                {
                    "weekday": 2,
                    "period_begin": "8:00",
                    "period_end": "22:00",
                },
            ],
            "exceptional_openings": [
                {
                    "period_begin": "2022-01-01T00:00:00+00:00",
                    "period_end": "2022-01-02T00:00:00+00:00",
                },
            ],
            "exceptional_closings": [],
        },
        "charging_when_closed": False,
        "images": [
            {
                "url": "https://www.example.com",
                "thumbnail": "https://www.example.com",
                "category": "CHARGER",
                "type": "type",
                "width": 10,
                "height": 10,
            },
        ],
        "energy_mix": {
            "is_green_energy": True,
            "energy_sources": [
                {"source": "SOLAR", "percentage": 100},
            ],
            "supplier_name": "supplier_name",
            "energy_product_name": "energy_product_name",
        },
        "last_updated": "2022-01-02 00:00:00+00:00",
    }
]


class Crud:
    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ):
        return LOCATIONS[0]

    @classmethod
    async def update(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        data: dict,
        id,
        *args,
        **kwargs,
    ):
        return data

    @classmethod
    async def create(
        cls, module: enums.ModuleID, role: enums.RoleEnum, data: dict, *args, **kwargs
    ):
        return data

    @classmethod
    async def list(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        filters: dict,
        *args,
        **kwargs,
    ) -> list:
        return LOCATIONS, 1, True


class Adapter:
    @classmethod
    def location_adapter(
        cls, data, version: VersionNumber = VersionNumber.latest
    ) -> Location:
        return Location(**data)


def test_cpo_get_locations_v_2_2_1():

    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    client = TestClient(app)
    response = client.get("/ocpi/cpo/2.2.1/locations")

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["id"] == LOCATIONS[0]["id"]


def test_cpo_get_location_v_2_2_1():

    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    client = TestClient(app)
    response = client.get(f'/ocpi/cpo/2.2.1/locations/{LOCATIONS[0]["id"]}')

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == LOCATIONS[0]["id"]


def test_cpo_get_evse_v_2_2_1():

    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    client = TestClient(app)
    response = client.get(
        f'/ocpi/cpo/2.2.1/locations/{LOCATIONS[0]["id"]}/{LOCATIONS[0]["evses"][0]["uid"]}'
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["uid"] == LOCATIONS[0]["evses"][0]["uid"]


def test_cpo_get_connector_v_2_2_1():

    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    client = TestClient(app)
    response = client.get(
        f'/ocpi/cpo/2.2.1/locations/{LOCATIONS[0]["id"]}/{LOCATIONS[0]["evses"][0]["uid"]}'
        f'/{LOCATIONS[0]["evses"][0]["connectors"][0]["id"]}'
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert (
        response.json()["data"][0]["id"]
        == LOCATIONS[0]["evses"][0]["connectors"][0]["id"]
    )


def test_emsp_get_location_v_2_2_1():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.emsp], Crud, Adapter)

    client = TestClient(app)
    response = client.get(
        f"/ocpi/emsp/2.2.1/locations/{settings.COUNTRY_CODE}/{settings.PARTY_ID}"
        f'/{LOCATIONS[0]["id"]}'
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == LOCATIONS[0]["id"]


def test_emsp_get_evse_v_2_2_1():

    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.emsp], Crud, Adapter)

    client = TestClient(app)
    response = client.get(
        f"/ocpi/emsp/2.2.1/locations/{settings.COUNTRY_CODE}/{settings.PARTY_ID}"
        f'/{LOCATIONS[0]["id"]}/{LOCATIONS[0]["evses"][0]["uid"]}'
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["uid"] == LOCATIONS[0]["evses"][0]["uid"]


def test_emsp_get_connector_v_2_2_1():

    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.emsp], Crud, Adapter)

    client = TestClient(app)
    response = client.get(
        f"/ocpi/emsp/2.2.1/locations/{settings.COUNTRY_CODE}/{settings.PARTY_ID}"
        f'/{LOCATIONS[0]["id"]}/{LOCATIONS[0]["evses"][0]["uid"]}'
        f'/{LOCATIONS[0]["evses"][0]["connectors"][0]["id"]}'
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert (
        response.json()["data"][0]["id"]
        == LOCATIONS[0]["evses"][0]["connectors"][0]["id"]
    )


def test_emsp_add_location_v_2_2_1():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.emsp], Crud, Adapter)

    client = TestClient(app)
    response = client.put(
        f"/ocpi/emsp/2.2.1/locations/{settings.COUNTRY_CODE}/{settings.PARTY_ID}"
        f'/{LOCATIONS[0]["id"]}',
        json=LOCATIONS[0],
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == LOCATIONS[0]["id"]


def test_emsp_add_evse_v_2_2_1():

    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.emsp], Crud, Adapter)

    client = TestClient(app)
    response = client.put(
        f"/ocpi/emsp/2.2.1/locations/{settings.COUNTRY_CODE}/{settings.PARTY_ID}"
        f'/{LOCATIONS[0]["id"]}/{LOCATIONS[0]["evses"][0]["uid"]}',
        json=LOCATIONS[0]["evses"][0],
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["uid"] == LOCATIONS[0]["evses"][0]["uid"]


def test_emsp_add_connector_v_2_2_1():

    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.emsp], Crud, Adapter)

    client = TestClient(app)
    response = client.put(
        f"/ocpi/emsp/2.2.1/locations/{settings.COUNTRY_CODE}/{settings.PARTY_ID}"
        f'/{LOCATIONS[0]["id"]}/{LOCATIONS[0]["evses"][0]["uid"]}'
        f'/{LOCATIONS[0]["evses"][0]["connectors"][0]["id"]}',
        json=LOCATIONS[0]["evses"][0]["connectors"][0],
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert (
        response.json()["data"][0]["id"]
        == LOCATIONS[0]["evses"][0]["connectors"][0]["id"]
    )


def test_emsp_patch_location_v_2_2_1():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.emsp], Crud, Adapter)

    patch_data = {"id": str(uuid4())}
    client = TestClient(app)
    response = client.patch(
        f"/ocpi/emsp/2.2.1/locations/{settings.COUNTRY_CODE}/{settings.PARTY_ID}"
        f'/{LOCATIONS[0]["id"]}',
        json=patch_data,
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == patch_data["id"]


def test_emsp_patch_evse_v_2_2_1():

    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.emsp], Crud, Adapter)

    patch_data = {"uid": str(uuid4())}
    client = TestClient(app)
    response = client.patch(
        f"/ocpi/emsp/2.2.1/locations/{settings.COUNTRY_CODE}/{settings.PARTY_ID}"
        f'/{LOCATIONS[0]["id"]}/{LOCATIONS[0]["evses"][0]["uid"]}',
        json=patch_data,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["uid"] == patch_data["uid"]


def test_emsp_patch_connector_v_2_2_1():

    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.emsp], Crud, Adapter)

    patch_data = {"id": str(uuid4())}
    client = TestClient(app)
    response = client.patch(
        f"/ocpi/emsp/2.2.1/locations/{settings.COUNTRY_CODE}/{settings.PARTY_ID}"
        f'/{LOCATIONS[0]["id"]}/{LOCATIONS[0]["evses"][0]["uid"]}'
        f'/{LOCATIONS[0]["evses"][0]["connectors"][0]["id"]}',
        json=patch_data,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["id"] == patch_data["id"]
