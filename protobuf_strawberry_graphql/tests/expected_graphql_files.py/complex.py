from enum import Enum


import strawberry


@strawberry.type
class ComplexMessage:
    @strawberry.type
    class N5:
        @strawberry.enum
        class N5Types(Enum):
            DEFAULT = 0
            type1 = 1
            type2 = 2
            type3 = 3
        types: 'ComplexMessage.N5.N5Types'
        data: 'str'

    @strawberry.type
    class RawMsgsByIdEntry:
        key: 'str'
        value: 'common.RawMsg'

    @strawberry.type
    class N4sByIdEntry:
        key: 'str'
        value: 'N4'

    @strawberry.type
    class N5sByIdEntry:
        key: 'str'
        value: 'ComplexMessage.N5'
    raw_msgs_by_id: 'ComplexMessage.RawMsgsByIdEntry'
    n4s: 'N4'
    n4s_by_id: 'ComplexMessage.N4sByIdEntry'
    n5s_by_id: 'ComplexMessage.N5sByIdEntry'


@strawberry.type
class common:
    @strawberry.type
    class RawMsg:
        timestamp: 'int'
        data: 'str'
        id: 'int'


@strawberry.type
class N4:
    @strawberry.type
    class RawMsgsByIdEntry:
        key: 'str'
        value: 'common.RawMsg'
    id: 'int'
    raw_msgs: 'common.RawMsg'
    raw_msgs_by_id: 'N4.RawMsgsByIdEntry'
