from collections import OrderedDict
import logging
from typing import Dict, Union, Optional, List, Iterable

import google
from google.protobuf.descriptor import FieldDescriptor


_LOGGER = logging.getLogger(__name__)
PYTHON_TAB = '    '


MessageMeta = google._upb._message.MessageMeta
ScalarMapContainer = google._upb._message.ScalarMapContainer
MessageMapContainer = google._upb._message.MessageMapContainer
Descriptor = google._upb._message.Descriptor
EnumDescriptor = google._upb._message.EnumDescriptor


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


# TODO:
# - support processing a collection of message definitions
#  (consider if requiring common objects not be duplicates is worth it)
# - try splitting this code up some more and add more comments
# - add commandline interface to this tool

def definitions_to_type(definitions: Iterable[MessageMeta]) -> Iterable[str]:
    # - support processing a collection of message definitions
    #  (consider if requiring common objects not be duplicates is worth it)
    pass


def definitions_to_reference_type(definitions: Iterable[MessageMeta]) -> Iterable[str]:
    # - support processing a collection of message definitions
    #  (consider if requiring common objects not be duplicates is worth it)
    pass


def definition_tree_to_reference_type(definition_tree: DescriptorWrapper) -> str:
    def descriptor_to_class_str(
            descriptor: 'Descriptor', nested_types: List[str] = [], depth=0) -> str:
        indent = PYTHON_TAB*depth
        if isinstance(descriptor, EnumDescriptor):
            definition_tree.import_enum = True
            return _enum_descriptor_to_str(descriptor, tabs=depth)
        else:
            class_def_str = f'{indent}@strawberry.type\n{indent}class {descriptor.name}:\n\n'
            class_def_str += _reference_type_create_method_definition(descriptor, tabs=depth+1)
            class_def_str += f'\n\n{indent + PYTHON_TAB}def __init__(self, proto):'
            class_def_str += f'\n{indent + PYTHON_TAB*2}self.proto = proto\n'
            if nested_types:
                class_def_str += '\n' + '\n\n'.join(nested_types)
            for field in descriptor.fields:
                class_def_str += f'\n{_reference_type_field_to_method_definition(field, tabs=depth+1)}\n'
            class_def_str += f'\n{_reference_type_update_method_definition(descriptor, tabs=depth+1)}\n'
            return class_def_str

    def file_tree_to_str(name: str, curr_node: DescriptorWrapper, depth=0) -> str:
        if not curr_node.children:
            if curr_node.descriptor:
                return descriptor_to_class_str(curr_node.descriptor, depth=depth)
            else:
                indent = depth*PYTHON_TAB
                return f"{indent}@strawberry.type\n{indent}class {name}:\npass"

        children = []
        for name_, child in curr_node.children.items():
            children.append(file_tree_to_str(name_, child, depth=depth+1))
        if curr_node.descriptor:
            return descriptor_to_class_str(curr_node.descriptor, nested_types=children, depth=depth)
        else:
            indent = depth*PYTHON_TAB
            nested_types = '\n'.join(children)
            return f"{indent}@strawberry.type\n{indent}class {name}:\n{nested_types}"

    children = []
    for name, child in definition_tree.children.items():
        children.append(file_tree_to_str(name, child))

    header = 'from typing import List\n\n\nimport strawberry\n\n\n'
    header = f'from enum import Enum\n{header}' if definition_tree.import_enum else header
    content = '\n\n\n'.join(children)
    return f'{header}{content}\n'


def definition_tree_to_relay_type(definition_tree: DescriptorWrapper) -> str:
    def descriptor_to_class_str(
            descriptor: 'Descriptor', nested_types: List[str] = [], depth=0) -> str:
        indent = PYTHON_TAB*depth
        if isinstance(descriptor, EnumDescriptor):
            definition_tree.import_enum = True
            return _enum_descriptor_to_str(descriptor, tabs=depth)
        else:
            class_def_str = f'{indent}@strawberry.type\n{indent}class {descriptor.name}:\n'
            class_def_str += _relay_type_create_method_definition(descriptor, tabs=depth+1)
            indent += PYTHON_TAB
            if nested_types:
                class_def_str += '\n' + '\n'.join(nested_types) + '\n'
            for field in descriptor.fields:
                field_str = _field_to_str(field)
                class_def_str += f'\n{indent}{field_str}'
            class_def_str += f'\n{_relay_type_update_method_definition(descriptor, tabs=depth+1)}\n'
            return class_def_str

    def file_tree_to_str(name: str, curr_node: DescriptorWrapper, depth=0) -> str:
        if not curr_node.children:
            if curr_node.descriptor:
                return descriptor_to_class_str(curr_node.descriptor, depth=depth)
            else:
                indent = depth*PYTHON_TAB
                return f"{indent}@strawberry.type\n{indent}class {name}:\npass"

        children = []
        for name_, child in curr_node.children.items():
            children.append(file_tree_to_str(name_, child, depth=depth+1))
        if curr_node.descriptor:
            return descriptor_to_class_str(curr_node.descriptor, nested_types=children, depth=depth)
        else:
            indent = depth*PYTHON_TAB
            nested_types = '\n'.join(children)
            return f"{indent}@strawberry.type\n{indent}class {name}:\n{nested_types}"

    children = []
    for name, child in definition_tree.children.items():
        children.append(file_tree_to_str(name, child))

    header = 'from typing import List\n\n\nimport strawberry\n\n\n'
    header = f'from enum import Enum\n{header}' if definition_tree.import_enum else header
    content = '\n\n'.join(children)
    return f'{header}{content}\n'


def create_definition_tree(definition: 'MessageMeta') -> DescriptorWrapper:
    # cost is needing to create a new or updating every prop on the object every time a new proto
    # comes in

    # need a global tree representing type definitions
    filetree = DescriptorWrapper()
    filetree.import_enum = False

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
    return filetree


# region Private Methods
def _reference_type_create_method_definition(descriptor: Descriptor, tabs=1) -> str:
    indent = PYTHON_TAB * tabs
    method_str = f'{indent}@staticmethod'
    method_str += f'\n{indent}def create_from_proto(proto) -> "{descriptor.full_name}":'
    method_str += f'\n{indent + PYTHON_TAB}return {descriptor.full_name}(proto)'
    return method_str


def _reference_type_update_method_definition(descriptor: Descriptor, tabs=1) -> str:
    indent = PYTHON_TAB * tabs
    method_str = f'{indent}def update(self, proto) -> "{descriptor.full_name}":'
    method_str += f'\n{indent + PYTHON_TAB}self.proto = proto'
    return method_str


def _relay_type_create_method_definition(descriptor: Descriptor, tabs=1) -> str:
    indent = PYTHON_TAB * tabs
    method_str = f'{indent}@staticmethod'
    method_str += f'\n{indent}def create_from_proto(proto) -> "{descriptor.full_name}":'
    indent += PYTHON_TAB
    args_str = ''
    args_indent = indent + PYTHON_TAB
    for field in descriptor.fields:
        if field.type == FieldDescriptor.TYPE_MESSAGE:
            if field.label != FieldDescriptor.LABEL_REPEATED:
                args_str += f'\n{args_indent}{field.name}='
                args_str += f'{field.message_type.full_name}.create_from_proto(proto.{field.name}),'
            elif field.message_type.GetOptions().map_entry:  # is a map:
                args_str += f'\n{args_indent}{field.name}=['
                args_str += f'{field.message_type.full_name}(key=k, value=v)'
                args_str += f' for k, v in proto.{field.name}.items()],'
            else:
                args_str += f'\n{args_indent}{field.name}=['
                args_str += f'{field.message_type.full_name}.create_from_proto(v) for v in proto.{field.name}],'
        else:
            args_str += f'\n{args_indent}{field.name}=proto.{field.name},'

    method_str += f'\n{indent}return {descriptor.full_name}({args_str}\n{indent})\n'
    return method_str


def _relay_type_update_method_definition(descriptor: Descriptor, tabs=1) -> str:
    indent = PYTHON_TAB * tabs
    method_str = f'\n{indent}def update(self, proto) -> "{descriptor.full_name}":'
    indent += PYTHON_TAB
    for field in descriptor.fields:
        if field.type == FieldDescriptor.TYPE_MESSAGE:
            if field.label != FieldDescriptor.LABEL_REPEATED:
                method_str += f'\n{indent}self.{field.name} = '
                method_str += f'{field.message_type.full_name}.update(proto.{field.name})'
            elif field.message_type.GetOptions().map_entry:  # is a map:
                method_str += f'\n{indent}self.{field.name} = ['
                method_str += f'{field.message_type.full_name}(key=k, value=v)'
                method_str += f' for k, v in proto.{field.name}.items()],'
            else:
                method_str += f'\n{indent}self.{field.name} = ['
                method_str += f'{field.message_type.full_name}.create_from_proto(v)'
                method_str += f' for v in proto.{field.name}],'
        else:
            method_str += f'\n{indent}self.{field.name}=proto.{field.name}'
    return method_str


def _enum_descriptor_to_str(enum_descriptor: EnumDescriptor, tabs=1) -> str:
    indent = PYTHON_TAB * tabs
    enum_def_str = f'{indent}@strawberry.enum\n{indent}class {enum_descriptor.name}(Enum):'
    indent += PYTHON_TAB
    for value in enum_descriptor.values:
        enum_def_str += f'\n{indent}{value.name} = {value.number}'
    return enum_def_str


def _get_field_type(field: FieldDescriptor) -> Optional[str]:
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
            _LOGGER.warning(f"field type: {field.type} not supported. ignoring.")
            return None
    return f'List[{field_type}]' if field.label == FieldDescriptor.LABEL_REPEATED else field_type


def _reference_type_field_to_method_definition(field: FieldDescriptor, tabs=1) -> str:
    indent = PYTHON_TAB * tabs
    field_type = _get_field_type(field)
    if field_type is None:
        return ''
    indent_p = indent + PYTHON_TAB
    str_ = f'{indent}@strawberry.field\n{indent}def {field.name}(self) -> {field_type}:'
    if field.type == FieldDescriptor.TYPE_MESSAGE:
        name = field.name
        if field.label != FieldDescriptor.LABEL_REPEATED:
            str_ += f'\n{indent_p}return {field.message_type.full_name}(self.proto.{name})'
            return str_
        elif field.message_type.GetOptions().map_entry:  # is a map:
            str_ += f'\n{indent_p}return [{field.message_type.full_name}(key=k, value=v)'
            str_ += f' for k, v in self.proto.{name}.items()]'
            return str_
        else:
            str_ += f'\n{indent_p}return ['
            str_ += f'{field.message_type.full_name}(v)'
            str_ += f' for v in self.proto.{field.name}],'
            return str_
    else:
        return f'{str_}\n{indent_p}return self.proto.{field.name}'


def _field_to_str(field: FieldDescriptor) -> str:
    """Converts field descriptor for a protobuf object to its graphql string representation.
    Args:
        field (FieldDescriptor): field descriptor to convert to string.
    Returns:
        str: field graphql string representation.
    """
    field_type = _get_field_type(field)
    return f"{field.name}: '{field_type}'" if field_type is not None else ''
# endregion
