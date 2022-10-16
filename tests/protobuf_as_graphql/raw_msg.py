import strawberry


@strawberry.type
class RawMsg:
    id: int
    timestamp: int
    data: str


def proto_to_graphql(msg) -> RawMsg:
    return RawMsg(msg.id, msg.timestamp, msg.data)
