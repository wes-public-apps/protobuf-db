from io import TextIOWrapper
from collections import OrderedDict
from pathlib import Path
import tempfile
from typing import Any, Iterator, Tuple, Dict

from google.protobuf.any_pb2 import Any as ProtoAny

from protobuf_utility.transforms.list_transformer import flatten_proto_to_list


# region Public Methods
def flatten_proto_to_csv(obj: ProtoAny) -> Tuple[str, str]:
    """Flattens a protobuf object into csv lines. It uses the flatten proto to list method to
    get the provided object as a list of attributes and values, then joins those lists into a
    comma separated string.
    Args:
        obj (ProtoAny): protobuf object to convert to csv lines.
    Returns:
        Tuple[str, str]: csv string of attributes and values.
    """
    attrs, values = flatten_proto_to_list(obj)

    # convert bytes to hex string
    for idx, value in enumerate(values):
        if isinstance(value, bytes):
            values[idx] = value.hex(' ')

    return ','.join(attrs), ','.join(map(str, values))


def flatten_same_proto_stream_to_csv(objs: Iterator, file_path: Path) -> Path:
    """Writes a stream of protobuf objects of the same type to a file. It uses the protobuf to list
    method to get the provided objects attributes and values in a list format. The content for each
    list is converted to a string and joined with a comma separator. That is then written to a
    file. This does additional work to post process the file to handle dynamically changing message
    sizes due to list or dictionary fields.
    Args:
        objs (Iterator): iterator of same type protobuf objects to convert to csv.
        file_path (Path): file path to write csv data to.
    Returns:
        Path: path to file containing csv content.
    """
    running_entry = OrderedDict()
    temp_file_name = None

    # write provided objects to temporary csv file
    with tempfile.NamedTemporaryFile('w', delete=False) as csv_f:
        temp_file_name = csv_f.name
        for object in objs:
            _proto_to_csv_file_helper(object, running_entry, csv_f)
    return _post_process_csv(','.join(running_entry.keys()), temp_file_name, file_path)


def flatten_mixed_proto_stream_to_csv(objs: Iterator, output_dir: Path) -> bool:
    """Writes a stream of protobuf objects to a file. It uses the protobuf to list method to get
    the provided object's attributes and values in a list format. The content for each list is
    converted to a string and joined with a comma separator. That is then written to a file for
    this specific object type. This method does additional work to post process the files to
    handle dynamically changing message sizes due to list or dictionary fields.
    Args:
        objs (Iterator): iterator of same type protobuf objects to convert to csv.
        file_path (Path): file path to write csv data to.
    Returns:
        Path: path to file containing csv content.
    """
    # Add helper items for tracking metadata for a specific stream type.
    class StreamContext:
        def __init__(self) -> None:
            self.running_entry = OrderedDict()
            self.temp_file = tempfile.NamedTemporaryFile('w', delete=False)
            self.line_count = 0

        def __del__(self) -> None:
            self.temp_file.close()
    stream_type_to_context: Dict[str, StreamContext] = {}

    # iterate over provided data stream and handle each stream type in its own context
    for obj in objs:
        stream_type = obj.DESCRIPTOR.full_name
        if stream_type in stream_type_to_context:
            pass
        else:
            stream_type_to_context[stream_type] = StreamContext()
        stream_type_to_context[stream_type].line_count += 1
        if stream_type == 'N4':
            print(stream_type_to_context[stream_type].temp_file.name)
        _proto_to_csv_file_helper(
            obj,
            stream_type_to_context[stream_type].running_entry,
            stream_type_to_context[stream_type].temp_file,
        )

    # add header to top of each data stream file
    for stream_type, context in stream_type_to_context.items():
        if stream_type == 'N4':
            print(output_dir / f'{stream_type}.csv')
        context.temp_file.close()
        _post_process_csv(
            ','.join(map(str, context.running_entry.keys())),
            context.temp_file.name,
            output_dir / f'{stream_type}.csv')
# endregion


# region Private Methods
def _post_process_csv(header: str, src_file: Path, dest_file: Path) -> Path:
    # add the header to the top of the ouptut file and then copy the data from the temporary file
    # this must be completed after writting the data because repeated elements make the header
    # values dynamic
    col_count = len(header.split(','))
    with open(src_file, 'r') as temp_csv_f:
        with open(dest_file, 'w') as csv_f:
            csv_f.write(f'{header}\n')
            for line in temp_csv_f:
                line_col_count = len(line.split(','))
                num_commas_to_add = col_count - line_col_count
                line = line[:-1] + ','*num_commas_to_add + '\n'
                csv_f.write(line)
    return dest_file


def _proto_to_csv_file_helper(obj: Any, running_entry: OrderedDict, csv_f: TextIOWrapper):
    # need to handle attrs changing for each object if they contain lists or dict
    # (need to consolidate indexes)
    attrs, values = flatten_proto_to_list(obj)
    for attr, value in zip(attrs, values):
        running_entry[attr] = value
    for key in running_entry.keys():
        if key not in attrs:
            running_entry[key] = ''
    line = ','.join(map(str, running_entry.values()))
    csv_f.write(f'{line}\n')
# endregion
