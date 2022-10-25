import google
from google.protobuf.descriptor import FieldDescriptor

MessageMeta = google._upb._message.MessageMeta
ScalarMapContainer = google._upb._message.ScalarMapContainer
MessageMapContainer = google._upb._message.MessageMapContainer
Descriptor = google._upb._message.Descriptor


def proto_definition_to_graphql_query(proto_def: MessageMeta) -> str:
    """Generated the client side graphql query for protobuf object as a string.
    Args:
        proto_def (MessageMeta): protobuf class to convert to a query.
    Returns:
        str: protobuf query
    """
    return _proto_definition_to_graphql_query(proto_def.DESCRIPTOR)


def _proto_definition_to_graphql_query(proto_descriptor: Descriptor, depth=1) -> str:
    # Sort fields based on number to provide a more reproducible order
    # Unsorted order matches that of file definition order even though there is no change to the
    # underlying protobuf if a field is moved. This makes the code unnecessarily unstable.
    field_nums = []
    fields = []
    for field in proto_descriptor.fields:
        field_nums.append(field.number)
        fields.append(field)
    id_fields = zip(field_nums, fields)
    sorted_id_fields = sorted(id_fields)

    query = '{'
    for _, field in sorted_id_fields:
        tab_str = "\t"*depth

        # Works completely for: scalars, list of scalars
        # Forms base for: nest messages, repeated messages, dictionaries
        query += f'\n{tab_str}{field.name}'

        # Handle nested messages
        if field.type == FieldDescriptor.TYPE_MESSAGE:
            query += ' '
            query += _proto_definition_to_graphql_query(field.message_type, depth=depth+1)

    return f'{query}\n{tab_str[:-1]}' + '}'
