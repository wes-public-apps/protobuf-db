import strawberry

from .raw_msg import RawMsg


@strawberry.type
class MapIntRawMsg:
    key: int
    value: RawMsg
