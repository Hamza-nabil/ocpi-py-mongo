from ocpi import get_application
from ocpi.core import enums
from ocpi.modules.versions.enums import VersionNumber


def test_get_application():
    class Crud: ...

    class Adapter: ...

    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    assert app.url_path_for("get_versions") == "/ocpi/versions"
