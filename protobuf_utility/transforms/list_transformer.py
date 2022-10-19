from typing import List, Tuple

import google
from google.protobuf.any_pb2 import Any as ProtoAny
from google.protobuf.descriptor import FieldDescriptor


def flatten_proto_to_list(obj: ProtoAny) -> Tuple[List, List]:
    """This method flattens a protobuf to a list. It follows the object tree as deep as it goes
    and creates a list of attributes and values. The attributes for nested items are formatted
    to match the syntax required to retrieve the value for that attribute from the object.
    Args:
        obj (ProtoAny): protobuf object to process.
    Returns:
        Tuple[List, List]: list of object attributes and list of object values.
    """
    attrs = []
    values = []

    # Sort fields based on number to provide a more reproducible order
    # Unsorted order matches that of file definition order even though there is no change to the
    # underlying protobuf if a field is moved. This makes the code unnecessarily unstable.
    sorted_fields = sorted(obj.DESCRIPTOR.fields, key=lambda f: f.number)

    for field in sorted_fields:
        value = getattr(obj, field.name)

        # Handle nested messages
        if field.type == FieldDescriptor.TYPE_MESSAGE:
            # Handle single nested message
            if field.label != FieldDescriptor.LABEL_REPEATED:
                nested_attrs, nested_values = flatten_proto_to_list(value)
                nested_attrs = [f'{field.name}.{attr}' for attr in nested_attrs]
                values.extend(nested_values)
                attrs.extend(nested_attrs)
                continue

            # Handle scalar map
            if isinstance(value,  google._upb._message.ScalarMapContainer):
                # map order cannot be guaranteed so to support as much consistency as possible
                # for maps that have fixed structures, sort the keys and use sorted order to
                # generate list.
                keys = list(value.keys())
                keys.sort()
                for key in keys:
                    attrs.append(f'{field.name}["{key}"]')
                    values.append(value[key])
                continue

            # Handle repeated nested message (map or list)
            if isinstance(value, google._upb._message.MessageMapContainer):
                generator = value.items()
            else:
                generator = enumerate(value)

            for idx, repeated_object in generator:
                nested_attrs, nested_values = flatten_proto_to_list(repeated_object)
                if type(idx) is str:
                    nested_attrs = [f'{field.name}["{idx}"].{attr}' for attr in nested_attrs]
                else:
                    nested_attrs = [f'{field.name}[{idx}].{attr}' for attr in nested_attrs]
                values.extend(nested_values)
                attrs.extend(nested_attrs)
            continue

        # Handle list of scalars
        if field.label == FieldDescriptor.LABEL_REPEATED:
            for idx, val in enumerate(value):
                values.append(val)
                attrs.append(f'{field.name}[{idx}]')
            continue

        # Handle scalars
        values.append(value)
        attrs.append(field.name)
    return attrs, values
