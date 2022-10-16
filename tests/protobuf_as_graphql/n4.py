from typing import List

import strawberry

from .raw_msg import RawMsg
from .map_int_raw_msg import MapIntRawMsg


@strawberry.type
class n4:
    id: int
    raw_msgs: List[RawMsg]
    raw_msgs_by_id: List[MapIntRawMsg]
