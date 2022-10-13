from pathlib import Path
import tempfile
from unittest import TestCase
import unittest

import test_data as td

from protobuf_utility.transforms.csv_transformer import flatten_mixed_proto_stream_to_csv
from protobuf_utility.transforms.csv_transformer import flatten_proto_to_csv
from protobuf_utility.transforms.csv_transformer import flatten_same_proto_stream_to_csv


class TestCSVTransformer(TestCase):

    def test_flatten_proto_to_csv_raw(self) -> None:
        # There is actually very little to test here since the complexity is in
        # flatten_proto_to_csv which is tested elsewhere.
        # We basically just have to verify we can successfully convert one message to a csv

        # Test Raw Msg
        attrs, values = flatten_proto_to_csv(td.raw_msg)
        self.assertEqual(attrs, "id,timestamp,data")
        self.assertEqual(values, f'{td.raw_msg.id},{td.raw_msg.timestamp},{td.raw_msg.data}')

    def test_flatten_proto_to_csv_types(self) -> None:
        # test a message with bytes data to verify it was formatted as a hex string
        attrs, values = flatten_proto_to_csv(td.test_types)
        self.assertEqual(attrs, ','.join([
            'val1',
            'val2',
            'val3',
            'val4',
            'val5',
            'val6',
            'val7',
            'val8',
            'val9',
            'val10',
            'val11',
            'val12',
            'val13',
            'val14',
            'val15',
            'val16',
            'val17.val1',
            'val17.val2',
            'val18["msg1"].val1',
            'val18["msg1"].val2',
            'val18["msg2"].val1',
            'val18["msg2"].val2',
            'val19[0].val1',
            'val19[0].val2',
            'val19[1].val1',
            'val19[1].val2',
            'val19[2].val1',
            'val19[2].val2',
        ]))
        self.assertEqual(values, ','.join(map(str, [
            td.test_types.val1,
            td.test_types.val2,
            td.test_types.val3,
            td.test_types.val4,
            td.test_types.val5,
            td.test_types.val6,
            td.test_types.val7,
            td.test_types.val8,
            td.test_types.val9,
            td.test_types.val10,
            td.test_types.val11,
            td.test_types.val12,
            td.test_types.val13,
            td.test_types.val14,
            td.test_types.val15.hex(' '),
            td.test_types.val16,
            td.test_types.val17.val1,
            td.test_types.val17.val2,
            td.test_types.val18["msg1"].val1,
            td.test_types.val18["msg1"].val2,
            td.test_types.val18["msg2"].val1,
            td.test_types.val18["msg2"].val2,
            td.test_types.val19[0].val1,
            td.test_types.val19[0].val2,
            td.test_types.val19[1].val1,
            td.test_types.val19[1].val2,
            td.test_types.val19[2].val1,
            td.test_types.val19[2].val2,
        ])))

    def test_flatten_mixed_protos_to_csv(self) -> None:
        stream = (
            td.raw_msg,
            td.n4,
            td.complex_msg,
            td.n6,
            td.n2,
            td.test_nested,
            td.test_specials,
            td.n3,
            td.test_types,
            td.n4_2,
            td.n4_3,
        )
        temp_dir = Path(tempfile.mkdtemp())
        flatten_mixed_proto_stream_to_csv(stream, temp_dir)

        # check all files exist
        created_files = [path.name for path in temp_dir.glob("*.csv")]
        for obj in stream:
            self.assertIn(f'{obj.DESCRIPTOR.full_name}.csv', created_files)

        # check N4
        self._check_n4_stream_to_csv(temp_dir / f'{td.n4.DESCRIPTOR.full_name}.csv')

    def test_flatten_same_protos_to_csv(self) -> None:
        stream = (
            td.n4,
            td.n4_2,
            td.n4_3,
        )
        file_path = Path(tempfile.mkdtemp()) / 'test_proto_transform.csv'
        flatten_same_proto_stream_to_csv(stream, file_path)

        # check all files exist
        self.assertTrue(file_path.exists())
        self._check_n4_stream_to_csv(file_path)

    def _check_n4_stream_to_csv(self, file_name):
        # check N4
        with open(file_name, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 4)
            # validate header
            self.assertEqual(
                lines[0].rstrip('\n'),
                ','.join([
                    'id',
                    'raw_msgs[0].id',
                    'raw_msgs[0].timestamp',
                    'raw_msgs[0].data',
                    'raw_msgs[1].id',
                    'raw_msgs[1].timestamp',
                    'raw_msgs[1].data',
                    'raw_msgs_by_id["msg0"].id',
                    'raw_msgs_by_id["msg0"].timestamp',
                    'raw_msgs_by_id["msg0"].data',
                    'raw_msgs_by_id["msg1"].id',
                    'raw_msgs_by_id["msg1"].timestamp',
                    'raw_msgs_by_id["msg1"].data',
                    'raw_msgs[2].id',
                    'raw_msgs[2].timestamp',
                    'raw_msgs[2].data',
                    'raw_msgs_by_id["a"].id',
                    'raw_msgs_by_id["a"].timestamp',
                    'raw_msgs_by_id["a"].data',
                ])
            )
            # test message type with variable size items
            self.assertEqual(lines[1].rstrip('\n'), ','.join(map(str, [
                td.n4.id,
                td.n4.raw_msgs[0].id,
                td.n4.raw_msgs[0].timestamp,
                td.n4.raw_msgs[0].data,
                td.n4.raw_msgs[1].id,
                td.n4.raw_msgs[1].timestamp,
                td.n4.raw_msgs[1].data,
                td.n4.raw_msgs_by_id["msg0"].id,
                td.n4.raw_msgs_by_id["msg0"].timestamp,
                td.n4.raw_msgs_by_id["msg0"].data,
                td.n4.raw_msgs_by_id["msg1"].id,
                td.n4.raw_msgs_by_id["msg1"].timestamp,
                td.n4.raw_msgs_by_id["msg1"].data,
                '', '', '',
                '', '', '',
            ])))
            self.assertEqual(lines[2].rstrip('\n'), ','.join(map(str, [
                td.n4_2.id,
                td.n4_2.raw_msgs[0].id,
                td.n4_2.raw_msgs[0].timestamp,
                td.n4_2.raw_msgs[0].data,
                td.n4_2.raw_msgs[1].id,
                td.n4_2.raw_msgs[1].timestamp,
                td.n4_2.raw_msgs[1].data,
                td.n4_2.raw_msgs_by_id["msg0"].id,
                td.n4_2.raw_msgs_by_id["msg0"].timestamp,
                td.n4_2.raw_msgs_by_id["msg0"].data,
                '', '', '',
                td.n4_2.raw_msgs[2].id,
                td.n4_2.raw_msgs[2].timestamp,
                td.n4_2.raw_msgs[2].data,
                td.n4_2.raw_msgs_by_id["a"].id,
                td.n4_2.raw_msgs_by_id["a"].timestamp,
                td.n4_2.raw_msgs_by_id["a"].data,
            ])))
            self.assertEqual(lines[3].rstrip('\n'), ','.join(map(str, [
                td.n4_3.id,
                td.n4_3.raw_msgs[0].id,
                td.n4_3.raw_msgs[0].timestamp,
                td.n4_3.raw_msgs[0].data,
                td.n4_3.raw_msgs[1].id,
                td.n4_3.raw_msgs[1].timestamp,
                td.n4_3.raw_msgs[1].data,
                td.n4_3.raw_msgs_by_id["msg0"].id,
                td.n4_3.raw_msgs_by_id["msg0"].timestamp,
                td.n4_3.raw_msgs_by_id["msg0"].data,
                td.n4_3.raw_msgs_by_id["msg1"].id,
                td.n4_3.raw_msgs_by_id["msg1"].timestamp,
                td.n4_3.raw_msgs_by_id["msg1"].data,
                td.n4_3.raw_msgs[2].id,
                td.n4_3.raw_msgs[2].timestamp,
                td.n4_3.raw_msgs[2].data,
                td.n4_3.raw_msgs_by_id["a"].id,
                td.n4_3.raw_msgs_by_id["a"].timestamp,
                td.n4_3.raw_msgs_by_id["a"].data,
            ])))


if __name__ == "__main__":
    unittest.main()
