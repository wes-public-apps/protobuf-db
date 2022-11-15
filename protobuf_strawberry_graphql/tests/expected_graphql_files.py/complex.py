from enum import Enum
from typing import List


import strawberry


@strawberry.type
class ComplexMessage:
    @staticmethod
    def create_from_proto(proto) -> "ComplexMessage":
        return ComplexMessage(
            raw_msgs_by_id=[ComplexMessage.RawMsgsByIdEntry(
                key=k, value=v) for k, v in proto.raw_msgs_by_id.items()],
            n4s=[N4.create_from_proto(v) for v in proto.n4s],
            n4s_by_id=[ComplexMessage.N4sByIdEntry(key=k, value=v)
                       for k, v in proto.n4s_by_id.items()],
            n5s_by_id=[ComplexMessage.N5sByIdEntry(key=k, value=v)
                       for k, v in proto.n5s_by_id.items()],
        )

    @strawberry.type
    class N5:
        @staticmethod
        def create_from_proto(proto) -> "ComplexMessage.N5":
            return ComplexMessage.N5(
                types=proto.types,
                data=proto.data,
            )

        @strawberry.enum
        class N5Types(Enum):
            DEFAULT = 0
            type1 = 1
            type2 = 2
            type3 = 3

        types: 'List[ComplexMessage.N5.N5Types]'
        data: 'str'

        def update(self, proto) -> "ComplexMessage.N5":
            self.types = proto.types
            self.data = proto.data

    @strawberry.type
    class RawMsgsByIdEntry:
        @staticmethod
        def create_from_proto(proto) -> "ComplexMessage.RawMsgsByIdEntry":
            return ComplexMessage.RawMsgsByIdEntry(
                key=proto.key,
                value=common.RawMsg.create_from_proto(proto.value),
            )

        key: 'str'
        value: 'common.RawMsg'

        def update(self, proto) -> "ComplexMessage.RawMsgsByIdEntry":
            self.key = proto.key
            self.value = common.RawMsg.update(proto.value)

    @strawberry.type
    class N4sByIdEntry:
        @staticmethod
        def create_from_proto(proto) -> "ComplexMessage.N4sByIdEntry":
            return ComplexMessage.N4sByIdEntry(
                key=proto.key,
                value=N4.create_from_proto(proto.value),
            )

        key: 'str'
        value: 'N4'

        def update(self, proto) -> "ComplexMessage.N4sByIdEntry":
            self.key = proto.key
            self.value = N4.update(proto.value)

    @strawberry.type
    class N5sByIdEntry:
        @staticmethod
        def create_from_proto(proto) -> "ComplexMessage.N5sByIdEntry":
            return ComplexMessage.N5sByIdEntry(
                key=proto.key,
                value=ComplexMessage.N5.create_from_proto(proto.value),
            )

        key: 'str'
        value: 'ComplexMessage.N5'

        def update(self, proto) -> "ComplexMessage.N5sByIdEntry":
            self.key = proto.key
            self.value = ComplexMessage.N5.update(proto.value)

    raw_msgs_by_id: 'List[ComplexMessage.RawMsgsByIdEntry]'
    n4s: 'List[N4]'
    n4s_by_id: 'List[ComplexMessage.N4sByIdEntry]'
    n5s_by_id: 'List[ComplexMessage.N5sByIdEntry]'

    def update(self, proto) -> "ComplexMessage":
        self.raw_msgs_by_id = [ComplexMessage.RawMsgsByIdEntry(
            key=k, value=v) for k, v in proto.raw_msgs_by_id.items()],
        self.n4s = [N4.create_from_proto(v) for v in proto.n4s],
        self.n4s_by_id = [ComplexMessage.N4sByIdEntry(
            key=k, value=v) for k, v in proto.n4s_by_id.items()],
        self.n5s_by_id = [ComplexMessage.N5sByIdEntry(
            key=k, value=v) for k, v in proto.n5s_by_id.items()],


@strawberry.type
class common:
    @strawberry.type
    class RawMsg:
        @staticmethod
        def create_from_proto(proto) -> "common.RawMsg":
            return common.RawMsg(
                timestamp=proto.timestamp,
                data=proto.data,
                id=proto.id,
            )

        timestamp: 'int'
        data: 'str'
        id: 'int'

        def update(self, proto) -> "common.RawMsg":
            self.timestamp = proto.timestamp
            self.data = proto.data
            self.id = proto.id


@strawberry.type
class N4:
    @staticmethod
    def create_from_proto(proto) -> "N4":
        return N4(
            id=proto.id,
            raw_msgs=[common.RawMsg.create_from_proto(v) for v in proto.raw_msgs],
            raw_msgs_by_id=[N4.RawMsgsByIdEntry(key=k, value=v)
                            for k, v in proto.raw_msgs_by_id.items()],
        )

    @strawberry.type
    class RawMsgsByIdEntry:
        @staticmethod
        def create_from_proto(proto) -> "N4.RawMsgsByIdEntry":
            return N4.RawMsgsByIdEntry(
                key=proto.key,
                value=common.RawMsg.create_from_proto(proto.value),
            )

        key: 'str'
        value: 'common.RawMsg'

        def update(self, proto) -> "N4.RawMsgsByIdEntry":
            self.key = proto.key
            self.value = common.RawMsg.update(proto.value)


    id: 'int'
    raw_msgs: 'List[common.RawMsg]'
    raw_msgs_by_id: 'List[N4.RawMsgsByIdEntry]'

    def update(self, proto) -> "N4":
        self.id = proto.id
        self.raw_msgs = [common.RawMsg.create_from_proto(v) for v in proto.raw_msgs],
        self.raw_msgs_by_id = [N4.RawMsgsByIdEntry(key=k, value=v)
                               for k, v in proto.raw_msgs_by_id.items()],


@strawberry.type
class ComplexMessage:

    @staticmethod
    def create_from_proto(proto) -> "ComplexMessage":
        return ComplexMessage(proto)

    def __init__(self, proto):
        self.proto = proto

    @strawberry.type
    class N5:

        @staticmethod
        def create_from_proto(proto) -> "ComplexMessage.N5":
            return ComplexMessage.N5(proto)

        def __init__(self, proto):
            self.proto = proto

        @strawberry.enum
        class N5Types(Enum):
            DEFAULT = 0
            type1 = 1
            type2 = 2
            type3 = 3

        @strawberry.field
        def types(self) -> List[ComplexMessage.N5.N5Types]:
            return self.proto.types

        @strawberry.field
        def data(self) -> str:
            return self.proto.data

        def update(self, proto) -> "ComplexMessage.N5":
            self.proto = proto

    @strawberry.type
    class RawMsgsByIdEntry:

        @staticmethod
        def create_from_proto(proto) -> "ComplexMessage.RawMsgsByIdEntry":
            return ComplexMessage.RawMsgsByIdEntry(proto)

        def __init__(self, proto):
            self.proto = proto

        @strawberry.field
        def key(self) -> str:
            return self.proto.key

        @strawberry.field
        def value(self) -> common.RawMsg:
            return common.RawMsg(self.proto.value)

        def update(self, proto) -> "ComplexMessage.RawMsgsByIdEntry":
            self.proto = proto

    @strawberry.type
    class N4sByIdEntry:

        @staticmethod
        def create_from_proto(proto) -> "ComplexMessage.N4sByIdEntry":
            return ComplexMessage.N4sByIdEntry(proto)

        def __init__(self, proto):
            self.proto = proto

        @strawberry.field
        def key(self) -> str:
            return self.proto.key

        @strawberry.field
        def value(self) -> N4:
            return N4(self.proto.value)

        def update(self, proto) -> "ComplexMessage.N4sByIdEntry":
            self.proto = proto

    @strawberry.type
    class N5sByIdEntry:

        @staticmethod
        def create_from_proto(proto) -> "ComplexMessage.N5sByIdEntry":
            return ComplexMessage.N5sByIdEntry(proto)

        def __init__(self, proto):
            self.proto = proto

        @strawberry.field
        def key(self) -> str:
            return self.proto.key

        @strawberry.field
        def value(self) -> ComplexMessage.N5:
            return ComplexMessage.N5(self.proto.value)

        def update(self, proto) -> "ComplexMessage.N5sByIdEntry":
            self.proto = proto

    @strawberry.field
    def raw_msgs_by_id(self) -> List[ComplexMessage.RawMsgsByIdEntry]:
        return [ComplexMessage.RawMsgsByIdEntry(key=k, value=v) for k, v in self.proto.raw_msgs_by_id.items()]

    @strawberry.field
    def n4s(self) -> List[N4]:
        return [N4(v) for v in self.proto.n4s],

    @strawberry.field
    def n4s_by_id(self) -> List[ComplexMessage.N4sByIdEntry]:
        return [ComplexMessage.N4sByIdEntry(key=k, value=v) for k, v in self.proto.n4s_by_id.items()]

    @strawberry.field
    def n5s_by_id(self) -> List[ComplexMessage.N5sByIdEntry]:
        return [ComplexMessage.N5sByIdEntry(key=k, value=v) for k, v in self.proto.n5s_by_id.items()]

    def update(self, proto) -> "ComplexMessage":
        self.proto = proto


@strawberry.type
class common:
    @strawberry.type
    class RawMsg:

        @staticmethod
        def create_from_proto(proto) -> "common.RawMsg":
            return common.RawMsg(proto)

        def __init__(self, proto):
            self.proto = proto

        @strawberry.field
        def timestamp(self) -> int:
            return self.proto.timestamp

        @strawberry.field
        def data(self) -> str:
            return self.proto.data

        @strawberry.field
        def id(self) -> int:
            return self.proto.id

        def update(self, proto) -> "common.RawMsg":
            self.proto = proto


@strawberry.type
class N4:

    @staticmethod
    def create_from_proto(proto) -> "N4":
        return N4(proto)

    def __init__(self, proto):
        self.proto = proto

    @strawberry.type
    class RawMsgsByIdEntry:

        @staticmethod
        def create_from_proto(proto) -> "N4.RawMsgsByIdEntry":
            return N4.RawMsgsByIdEntry(proto)

        def __init__(self, proto):
            self.proto = proto

        @strawberry.field
        def key(self) -> str:
            return self.proto.key

        @strawberry.field
        def value(self) -> common.RawMsg:
            return common.RawMsg(self.proto.value)

        def update(self, proto) -> "N4.RawMsgsByIdEntry":
            self.proto = proto

    @strawberry.field
    def id(self) -> int:
        return self.proto.id

    @strawberry.field
    def raw_msgs(self) -> List[common.RawMsg]:
        return [common.RawMsg(v) for v in self.proto.raw_msgs],

    @strawberry.field
    def raw_msgs_by_id(self) -> List[N4.RawMsgsByIdEntry]:
        return [N4.RawMsgsByIdEntry(key=k, value=v) for k, v in self.proto.raw_msgs_by_id.items()]

    def update(self, proto) -> "N4":
        self.proto = proto
