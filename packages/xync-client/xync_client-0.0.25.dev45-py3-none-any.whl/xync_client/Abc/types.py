from msgspec import Struct
from x_model.types import New
from xync_schema.enums import PmType
from xync_schema.models import Country, Pm, Ex
from xync_schema.types import PmexBank

from xync_client.pm_unifier import PmUni


class PmEx(Struct):
    exid: int | str
    name: str
    # todo: duplicates
    typ: PmType = None
    logo: str = None
    banks: list[PmexBank] = None


class PmIn(New, PmUni):
    _unq = "norm", "country"
    country: Country = None
    # todo: duplicates
    typ: PmType = None
    logo: str = None
    banks: list[PmexBank] = None


class PmExIn(Struct):
    pm = Pm
    ex = Ex
    exid = int | str
    name = str
