# proto definition to strawberry query

# handle nested message
# handle enum
# handle simple python type
# handle repeated simple
# handle repeated nested
# handle imported types
from collections import OrderedDict
import logging
from typing import Dict, Union, Optional, List

import google
from google.protobuf.descriptor import FieldDescriptor

from dataclasses import dataclass


_LOGGER = logging.getLogger(__name__)


MessageMeta = google._upb._message.MessageMeta
ScalarMapContainer = google._upb._message.ScalarMapContainer
MessageMapContainer = google._upb._message.MessageMapContainer
Descriptor = google._upb._message.Descriptor
EnumDescriptor = google._upb._message.EnumDescriptor


@dataclass
class DescriptorWrapper:
    def __init__(self, descriptor=None) -> None:
        self.children: Dict[str, 'DescriptorWrapper'] = OrderedDict()
        self.descriptor: Optional[Union[Descriptor, EnumDescriptor]] = descriptor


proto_type_to_python_type = {
    1: 'float',  # TYPE_DOUBLE
    2: 'float',  # TYPE_FLOAT
    3: 'long',  # TYPE_INT64
    4: 'long',  # TYPE_UINT64
    5: 'int',  # TYPE_INT32
    6: 'long',  # TYPE_FIXED64
    7: 'int',  # TYPE_FIXED32
    8: 'bool',  # TYPE_BOOL
    9: 'str',  # TYPE_STRING
    12: 'bytes',  # TYPE_BYTES
    13: 'int',  # TYPE_UINT32
    15: 'int',  # TYPE_SFIXED32
    16: 'long',  # TYPE_SFIXED64
    17: 'int',  # TYPE_SINT32
    18: 'long',  # TYPE_SINT64
}


def definition_to_query(definition: 'MessageMeta') -> str:
    # Hacks
    # - any dependency of current definition gets defined in the current file (aka duplicate definitions are ok)

    # need a global tree representing type definitions
    filetree = DescriptorWrapper()

    def add_descriptor(descriptor: Descriptor) -> None:

        def insert_descriptor(name: str, children: Dict[str, DescriptorWrapper]) -> None:
            if name not in children:
                children[name] = DescriptorWrapper(descriptor=descriptor)
            else:
                children[name].descriptor = descriptor

        names = descriptor.full_name.split('.')
        if descriptor.full_name == descriptor.name:
            insert_descriptor(descriptor.name, filetree.children)
        else:
            curr_node = filetree
            for name_ in names[:-1]:
                if name_ in curr_node.children:
                    pass
                else:
                    curr_node.children[name_] = DescriptorWrapper()
                curr_node = curr_node.children[name_]
            insert_descriptor(names[-1], curr_node.children)

    def construct_file_tree(descriptor: 'Descriptor') -> None:

        # handle descriptor tree location
        add_descriptor(descriptor)

        # nested enums
        for nested in descriptor.enum_types:
            add_descriptor(nested)
        # nested message
        for nested in descriptor.nested_types:
            construct_file_tree(nested)
        # referenced types
        for field in descriptor.fields:
            if field.type == FieldDescriptor.TYPE_MESSAGE:
                construct_file_tree(field.message_type)
            elif field.type == FieldDescriptor.TYPE_ENUM:
                add_descriptor(field.enum_type)
            else:
                # if not an enum or message type we do not need to define the type elsewhere
                # so no action necessary
                pass

    construct_file_tree(definition.DESCRIPTOR)

    def field_to_str(field: FieldDescriptor) -> str:
        # Complex Types
        # TODO: handle group
        if field.type == FieldDescriptor.TYPE_MESSAGE:
            field_type = field.message_type.full_name
        elif field.type == FieldDescriptor.TYPE_ENUM:
            field_type = field.enum_type.full_name
        # Python Types
        else:
            if field.type in proto_type_to_python_type:
                field_type = proto_type_to_python_type[field.type]
            else:
                field_type = ''
        return f"{field.name}: '{field_type}'"

    def descriptor_to_class_str(
            descriptor: Descriptor, nested_types: List[str] = [], depth=0) -> str:
        indent = '    '*depth
        if isinstance(descriptor, EnumDescriptor):
            enum_def_str = f'{indent}@strawberry.enum\n{indent}class {descriptor.name}(enum):'
            # TODO: loop over every value
            return enum_def_str
        else:
            class_def_str = f'{indent}@strawberry.type\n{indent}class {descriptor.name}:'
            indent += '    '
            if nested_types:
                class_def_str += '\n' + '\n\n'.join(nested_types)
            for field in descriptor.fields:
                field_str = field_to_str(field)
                class_def_str += f'\n{indent}{field_str}'
            return class_def_str

    def file_tree_to_str(name: str, curr_node: DescriptorWrapper, depth=0) -> str:
        if not curr_node.children:
            if curr_node.descriptor:
                return descriptor_to_class_str(curr_node.descriptor, depth=depth)
            else:
                indent = depth*'    '
                return f"{indent}@strawberry.type\n{indent}class {name}:\npass"

        children = []
        for name_, child in curr_node.children.items():
            children.append(file_tree_to_str(name_, child, depth=depth+1))
        if curr_node.descriptor:
            return descriptor_to_class_str(curr_node.descriptor, nested_types=children, depth=depth)
        else:
            indent = depth*'    '
            nested_types = '\n'.join(children)
            return f"{indent}@strawberry.type\n{indent}class {name}:\n{nested_types}"

    children = []
    for name, child in filetree.children.items():
        children.append(file_tree_to_str(name, child))
    return '\n\n\n'.join(children)
