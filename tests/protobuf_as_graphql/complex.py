import enum
from typing import List

import strawberry

from .n4 import n4
from .map_int_raw_msg import MapIntRawMsg
from .raw_msg import RawMsg


@strawberry.enum
class N5Types(enum):
    DEFAULT = 0
    type1 = 1
    type2 = 2
    type3 = 3


@strawberry.type
class n5:
    types: N5Types  # enum
    data: str


@strawberry
class MapStrn5:
    key: str
    value: n5


@strawberry.type
class ComplexMessage:
    raw_msgs_by_id = List[MapIntRawMsg]
    n4s = List[n4]
    n4s_by_id = List[]
    n5s_by_id = List[MapStrn5]
