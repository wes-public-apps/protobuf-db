from pathlib import Path
import tempfile
from unittest import TestCase
import unittest

from common_pb2 import RawMsg
from complex_pb2 import N4, N6, ComplexMessage
from nested_pb2 import N2, TestNested
from specials_pb2 import TestSpecials
from types_pb2 import N3, TestTypes, TYPES

from protobuf_utility.transforms.csv_transformer import flatten_mixed_proto_stream_to_csv
from protobuf_utility.transforms.csv_transformer import flatten_proto_to_csv
from protobuf_utility.transforms.csv_transformer import flatten_same_proto_stream_to_csv
from protobuf_utility.transforms.list_transformer import flatten_proto_to_list


class TestTransformers(TestCase):

    @classmethod
    def setUpClass(cls):
        # common raw msg
        def set_raw(obj, id=10, timestamp=23432, data="data"):
            obj.id = id
            obj.timestamp = timestamp
            obj.data = data

        cls.raw_msg = RawMsg()
        set_raw(cls.raw_msg)

        # complex n4
        def set_n4(obj, id=23):
            obj.id = 23
            obj.raw_msgs.extend([RawMsg(), RawMsg()])
            set_raw(obj.raw_msgs[0])
            set_raw(obj.raw_msgs[1], id=11)
            set_raw(obj.raw_msgs_by_id['msg0'])
            set_raw(obj.raw_msgs_by_id['msg1'], id=11)
        cls.n4 = N4()
        cls.n4_2 = N4()
        cls.n4_3 = N4()
        set_n4(cls.n4)
        set_n4(cls.n4_2)
        set_n4(cls.n4_3)
        cls.n4_2.raw_msgs.append(RawMsg())
        cls.n4_3.raw_msgs.append(RawMsg())
        set_raw(cls.n4_2.raw_msgs[2])
        set_raw(cls.n4_2.raw_msgs_by_id['a'])
        set_raw(cls.n4_3.raw_msgs[2])
        set_raw(cls.n4_3.raw_msgs_by_id['a'])
        del cls.n4_2.raw_msgs_by_id["msg1"]

        # complex complex
        cls.complex_msg = ComplexMessage()
        set_raw(cls.complex_msg.raw_msgs_by_id['msg0'])
        set_raw(cls.complex_msg.raw_msgs_by_id['msg1'], id=11)
        cls.complex_msg.n4s.extend([N4(), N4()])
        set_n4(cls.complex_msg.n4s[0])
        set_n4(cls.complex_msg.n4s[1], id=24)
        set_n4(cls.complex_msg.n4s_by_id['msg0'])
        set_n4(cls.complex_msg.n4s_by_id['msg1'], id=24)

        def set_n5(obj, types=[], data="n5_data"):
            obj.types.extend(types)
            obj.data = data

        set_n5(
            cls.complex_msg.n5s_by_id['msg0'],
            types=[
                ComplexMessage.N5.N5Types.Value('type1'),
                ComplexMessage.N5.N5Types.Value('type2')])
        set_n5(
            cls.complex_msg.n5s_by_id['msg1'],
            types=[
                ComplexMessage.N5.N5Types.Value('type1'),
                ComplexMessage.N5.N5Types.Value('type2')],
            data="n5_data_1")

        # complex N6
        cls.n6 = N6()
        set_n5(cls.n6.n5val)

        # nested N2
        cls.n2 = N2()
        cls.n2.val2 = "this is n2"

        # nested TestNested
        cls.test_nested = TestNested()
        cls.test_nested.val1.val1 = "this is a nested n1"
        cls.test_nested.val2.val2 = "this is a nested n2"

        # specials TestSpecial
        cls.test_specials = TestSpecials()
        cls.test_specials.list1.extend(["1", "2", "3"])
        cls.test_specials.map1["key1"] = "val1"
        cls.test_specials.map1["key2"] = "val2"
        cls.test_specials.map1["key3"] = "val3"
        cls.test_specials.fault1 = True

        # types N3
        cls.n3 = N3()
        cls.n3.val1 = 1
        cls.n3.val2 = 2

        # types TestTypes
        cls.test_types = TestTypes()
        cls.test_types.val1 = -320
        cls.test_types.val2 = 0.032
        cls.test_types.val3 = -24
        cls.test_types.val4 = -2439723
        cls.test_types.val5 = 32845
        cls.test_types.val6 = 89345230
        cls.test_types.val7 = -32932
        cls.test_types.val8 = 329323
        cls.test_types.val9 = 843782
        cls.test_types.val10 = 348795439
        cls.test_types.val11 = -329823
        cls.test_types.val12 = -329823238
        cls.test_types.val13 = False
        cls.test_types.val14 = "hello world"
        cls.test_types.val15 = b'jknq3290dskss'
        cls.test_types.val16 = TYPES.type1
        cls.test_types.val17.val1 = 1
        cls.test_types.val17.val2 = 2
        cls.test_types.val18["msg1"].val1 = 1
        cls.test_types.val18["msg1"].val2 = 2
        cls.test_types.val18['msg2'].val1 = 1
        cls.test_types.val18['msg2'].val2 = 1
        cls.test_types.val19.extend([N3(), N3(), N3()])

    def test_flatten_proto_to_list_raw_msg(self) -> None:
        # Test Raw Msg
        attrs, values = flatten_proto_to_list(self.raw_msg)
        self.assertEqual(attrs, ["id", "timestamp", "data"])
        self.assertEqual(values, [self.raw_msg.id, self.raw_msg.timestamp, self.raw_msg.data])

    def test_flatten_proto_to_list_n4(self) -> None:
        # Test N4
        attrs, values = flatten_proto_to_list(self.n4)
        self.assertEqual(attrs, [
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
        ])
        self.assertEqual(values, [
            self.n4.id,
            self.n4.raw_msgs[0].id,
            self.n4.raw_msgs[0].timestamp,
            self.n4.raw_msgs[0].data,
            self.n4.raw_msgs[1].id,
            self.n4.raw_msgs[1].timestamp,
            self.n4.raw_msgs[1].data,
            self.n4.raw_msgs_by_id["msg0"].id,
            self.n4.raw_msgs_by_id["msg0"].timestamp,
            self.n4.raw_msgs_by_id["msg0"].data,
            self.n4.raw_msgs_by_id["msg1"].id,
            self.n4.raw_msgs_by_id["msg1"].timestamp,
            self.n4.raw_msgs_by_id["msg1"].data,
        ])

    def test_flatten_proto_to_list_complex_message(self) -> None:
        # test complex
        attrs, values = flatten_proto_to_list(self.complex_msg)
        self.assertEqual(attrs, [
            'raw_msgs_by_id["msg0"].id',
            'raw_msgs_by_id["msg0"].timestamp',
            'raw_msgs_by_id["msg0"].data',
            'raw_msgs_by_id["msg1"].id',
            'raw_msgs_by_id["msg1"].timestamp',
            'raw_msgs_by_id["msg1"].data',
            'n4s[0].id',
            'n4s[0].raw_msgs[0].id',
            'n4s[0].raw_msgs[0].timestamp',
            'n4s[0].raw_msgs[0].data',
            'n4s[0].raw_msgs[1].id',
            'n4s[0].raw_msgs[1].timestamp',
            'n4s[0].raw_msgs[1].data',
            'n4s[0].raw_msgs_by_id["msg0"].id',
            'n4s[0].raw_msgs_by_id["msg0"].timestamp',
            'n4s[0].raw_msgs_by_id["msg0"].data',
            'n4s[0].raw_msgs_by_id["msg1"].id',
            'n4s[0].raw_msgs_by_id["msg1"].timestamp',
            'n4s[0].raw_msgs_by_id["msg1"].data',
            'n4s[1].id',
            'n4s[1].raw_msgs[0].id',
            'n4s[1].raw_msgs[0].timestamp',
            'n4s[1].raw_msgs[0].data',
            'n4s[1].raw_msgs[1].id',
            'n4s[1].raw_msgs[1].timestamp',
            'n4s[1].raw_msgs[1].data',
            'n4s[1].raw_msgs_by_id["msg0"].id',
            'n4s[1].raw_msgs_by_id["msg0"].timestamp',
            'n4s[1].raw_msgs_by_id["msg0"].data',
            'n4s[1].raw_msgs_by_id["msg1"].id',
            'n4s[1].raw_msgs_by_id["msg1"].timestamp',
            'n4s[1].raw_msgs_by_id["msg1"].data',
            'n4s_by_id["msg0"].id',
            'n4s_by_id["msg0"].raw_msgs[0].id',
            'n4s_by_id["msg0"].raw_msgs[0].timestamp',
            'n4s_by_id["msg0"].raw_msgs[0].data',
            'n4s_by_id["msg0"].raw_msgs[1].id',
            'n4s_by_id["msg0"].raw_msgs[1].timestamp',
            'n4s_by_id["msg0"].raw_msgs[1].data',
            'n4s_by_id["msg0"].raw_msgs_by_id["msg0"].id',
            'n4s_by_id["msg0"].raw_msgs_by_id["msg0"].timestamp',
            'n4s_by_id["msg0"].raw_msgs_by_id["msg0"].data',
            'n4s_by_id["msg0"].raw_msgs_by_id["msg1"].id',
            'n4s_by_id["msg0"].raw_msgs_by_id["msg1"].timestamp',
            'n4s_by_id["msg0"].raw_msgs_by_id["msg1"].data',
            'n4s_by_id["msg1"].id',
            'n4s_by_id["msg1"].raw_msgs[0].id',
            'n4s_by_id["msg1"].raw_msgs[0].timestamp',
            'n4s_by_id["msg1"].raw_msgs[0].data',
            'n4s_by_id["msg1"].raw_msgs[1].id',
            'n4s_by_id["msg1"].raw_msgs[1].timestamp',
            'n4s_by_id["msg1"].raw_msgs[1].data',
            'n4s_by_id["msg1"].raw_msgs_by_id["msg0"].id',
            'n4s_by_id["msg1"].raw_msgs_by_id["msg0"].timestamp',
            'n4s_by_id["msg1"].raw_msgs_by_id["msg0"].data',
            'n4s_by_id["msg1"].raw_msgs_by_id["msg1"].id',
            'n4s_by_id["msg1"].raw_msgs_by_id["msg1"].timestamp',
            'n4s_by_id["msg1"].raw_msgs_by_id["msg1"].data',
            'n5s_by_id["msg0"].types[0]',
            'n5s_by_id["msg0"].types[1]',
            'n5s_by_id["msg0"].data',
            'n5s_by_id["msg1"].types[0]',
            'n5s_by_id["msg1"].types[1]',
            'n5s_by_id["msg1"].data',
        ])
        self.assertEqual(values, [
            self.complex_msg.raw_msgs_by_id["msg0"].id,
            self.complex_msg.raw_msgs_by_id["msg0"].timestamp,
            self.complex_msg.raw_msgs_by_id["msg0"].data,
            self.complex_msg.raw_msgs_by_id["msg1"].id,
            self.complex_msg.raw_msgs_by_id["msg1"].timestamp,
            self.complex_msg.raw_msgs_by_id["msg1"].data,
            self.complex_msg.n4s[0].id,
            self.complex_msg.n4s[0].raw_msgs[0].id,
            self.complex_msg.n4s[0].raw_msgs[0].timestamp,
            self.complex_msg.n4s[0].raw_msgs[0].data,
            self.complex_msg.n4s[0].raw_msgs[1].id,
            self.complex_msg.n4s[0].raw_msgs[1].timestamp,
            self.complex_msg.n4s[0].raw_msgs[1].data,
            self.complex_msg.n4s[0].raw_msgs_by_id["msg0"].id,
            self.complex_msg.n4s[0].raw_msgs_by_id["msg0"].timestamp,
            self.complex_msg.n4s[0].raw_msgs_by_id["msg0"].data,
            self.complex_msg.n4s[0].raw_msgs_by_id["msg1"].id,
            self.complex_msg.n4s[0].raw_msgs_by_id["msg1"].timestamp,
            self.complex_msg.n4s[0].raw_msgs_by_id["msg1"].data,
            self.complex_msg.n4s[1].id,
            self.complex_msg.n4s[1].raw_msgs[0].id,
            self.complex_msg.n4s[1].raw_msgs[0].timestamp,
            self.complex_msg.n4s[1].raw_msgs[0].data,
            self.complex_msg.n4s[1].raw_msgs[1].id,
            self.complex_msg.n4s[1].raw_msgs[1].timestamp,
            self.complex_msg.n4s[1].raw_msgs[1].data,
            self.complex_msg.n4s[1].raw_msgs_by_id["msg0"].id,
            self.complex_msg.n4s[1].raw_msgs_by_id["msg0"].timestamp,
            self.complex_msg.n4s[1].raw_msgs_by_id["msg0"].data,
            self.complex_msg.n4s[1].raw_msgs_by_id["msg1"].id,
            self.complex_msg.n4s[1].raw_msgs_by_id["msg1"].timestamp,
            self.complex_msg.n4s[1].raw_msgs_by_id["msg1"].data,
            self.complex_msg.n4s_by_id["msg0"].id,
            self.complex_msg.n4s_by_id["msg0"].raw_msgs[0].id,
            self.complex_msg.n4s_by_id["msg0"].raw_msgs[0].timestamp,
            self.complex_msg.n4s_by_id["msg0"].raw_msgs[0].data,
            self.complex_msg.n4s_by_id["msg0"].raw_msgs[1].id,
            self.complex_msg.n4s_by_id["msg0"].raw_msgs[1].timestamp,
            self.complex_msg.n4s_by_id["msg0"].raw_msgs[1].data,
            self.complex_msg.n4s_by_id["msg0"].raw_msgs_by_id["msg0"].id,
            self.complex_msg.n4s_by_id["msg0"].raw_msgs_by_id["msg0"].timestamp,
            self.complex_msg.n4s_by_id["msg0"].raw_msgs_by_id["msg0"].data,
            self.complex_msg.n4s_by_id["msg0"].raw_msgs_by_id["msg1"].id,
            self.complex_msg.n4s_by_id["msg0"].raw_msgs_by_id["msg1"].timestamp,
            self.complex_msg.n4s_by_id["msg0"].raw_msgs_by_id["msg1"].data,
            self.complex_msg.n4s_by_id["msg1"].id,
            self.complex_msg.n4s_by_id["msg1"].raw_msgs[0].id,
            self.complex_msg.n4s_by_id["msg1"].raw_msgs[0].timestamp,
            self.complex_msg.n4s_by_id["msg1"].raw_msgs[0].data,
            self.complex_msg.n4s_by_id["msg1"].raw_msgs[1].id,
            self.complex_msg.n4s_by_id["msg1"].raw_msgs[1].timestamp,
            self.complex_msg.n4s_by_id["msg1"].raw_msgs[1].data,
            self.complex_msg.n4s_by_id["msg1"].raw_msgs_by_id["msg0"].id,
            self.complex_msg.n4s_by_id["msg1"].raw_msgs_by_id["msg0"].timestamp,
            self.complex_msg.n4s_by_id["msg1"].raw_msgs_by_id["msg0"].data,
            self.complex_msg.n4s_by_id["msg1"].raw_msgs_by_id["msg1"].id,
            self.complex_msg.n4s_by_id["msg1"].raw_msgs_by_id["msg1"].timestamp,
            self.complex_msg.n4s_by_id["msg1"].raw_msgs_by_id["msg1"].data,
            self.complex_msg.n5s_by_id["msg0"].types[0],
            self.complex_msg.n5s_by_id["msg0"].types[1],
            self.complex_msg.n5s_by_id["msg0"].data,
            self.complex_msg.n5s_by_id["msg1"].types[0],
            self.complex_msg.n5s_by_id["msg1"].types[1],
            self.complex_msg.n5s_by_id["msg1"].data,
        ])

    def test_flatten_proto_to_list_n6(self) -> None:
        # test n6
        attrs, values = flatten_proto_to_list(self.n6)
        self.assertEqual(attrs, [
            'n5val.data',
        ])
        self.assertEqual(values, [
            self.n6.n5val.data,
        ])

    def test_flatten_proto_to_list_n2(self) -> None:
        # test n2
        attrs, values = flatten_proto_to_list(self.n2)
        self.assertEqual(attrs, [
            'val2',
        ])
        self.assertEqual(values, [
            self.n2.val2,
        ])

    def test_flatten_proto_to_list_nested(self) -> None:
        # test nested
        attrs, values = flatten_proto_to_list(self.test_nested)
        self.assertEqual(attrs, [
            'val1.val1',
            'val2.val2',
        ])
        self.assertEqual(values, [
            self.test_nested.val1.val1,
            self.test_nested.val2.val2,
        ])

    def test_flatten_proto_to_list_specials(self) -> None:
        # test specials
        # dictionaries keys are sorted alphabetically
        attrs, values = flatten_proto_to_list(self.test_specials)
        self.assertEqual(attrs, [
            'list1[0]',
            'list1[1]',
            'list1[2]',
            'map1["key1"]',
            'map1["key2"]',
            'map1["key3"]',
            'fault1',
            'fault2',
        ])
        self.assertEqual(values, [
            self.test_specials.list1[0],
            self.test_specials.list1[1],
            self.test_specials.list1[2],
            self.test_specials.map1["key1"],
            self.test_specials.map1["key2"],
            self.test_specials.map1["key3"],
            self.test_specials.fault1,
            self.test_specials.fault2,
        ])

    def test_flatten_proto_to_list_n3(self) -> None:
        # test N3
        attrs, values = flatten_proto_to_list(self.n3)
        self.assertEqual(attrs, [
            'val1',
            'val2',
        ])
        self.assertEqual(values, [
            self.n3.val1,
            self.n3.val2,
        ])

    def test_flatten_proto_to_list_types(self) -> None:
        # test types
        attrs, values = flatten_proto_to_list(self.test_types)
        self.assertEqual(attrs, [
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
        ])
        self.assertEqual(values, [
            self.test_types.val1,
            self.test_types.val2,
            self.test_types.val3,
            self.test_types.val4,
            self.test_types.val5,
            self.test_types.val6,
            self.test_types.val7,
            self.test_types.val8,
            self.test_types.val9,
            self.test_types.val10,
            self.test_types.val11,
            self.test_types.val12,
            self.test_types.val13,
            self.test_types.val14,
            self.test_types.val15,
            self.test_types.val16,
            self.test_types.val17.val1,
            self.test_types.val17.val2,
            self.test_types.val18["msg1"].val1,
            self.test_types.val18["msg1"].val2,
            self.test_types.val18["msg2"].val1,
            self.test_types.val18["msg2"].val2,
            self.test_types.val19[0].val1,
            self.test_types.val19[0].val2,
            self.test_types.val19[1].val1,
            self.test_types.val19[1].val2,
            self.test_types.val19[2].val1,
            self.test_types.val19[2].val2,
        ])

        # TODO(wesley): Handle changing the location of a field in the protobuf but keep the id.
        # field order should be preserved.
        # if not sort by field id to determine order.

    def test_flatten_proto_to_csv_raw(self) -> None:
        # There is actually very little to test here since the complexity is in
        # flatten_proto_to_csv which is tested elsewhere.
        # We basically just have to verify we can successfully convert one message to a csv

        # Test Raw Msg
        attrs, values = flatten_proto_to_csv(self.raw_msg)
        self.assertEqual(attrs, "id,timestamp,data")
        self.assertEqual(values, f'{self.raw_msg.id},{self.raw_msg.timestamp},{self.raw_msg.data}')

    def test_flatten_proto_to_csv_types(self) -> None:
        # test a message with bytes data to verify it was formatted as a hex string
        attrs, values = flatten_proto_to_csv(self.test_types)
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
            self.test_types.val1,
            self.test_types.val2,
            self.test_types.val3,
            self.test_types.val4,
            self.test_types.val5,
            self.test_types.val6,
            self.test_types.val7,
            self.test_types.val8,
            self.test_types.val9,
            self.test_types.val10,
            self.test_types.val11,
            self.test_types.val12,
            self.test_types.val13,
            self.test_types.val14,
            self.test_types.val15.hex(' '),
            self.test_types.val16,
            self.test_types.val17.val1,
            self.test_types.val17.val2,
            self.test_types.val18["msg1"].val1,
            self.test_types.val18["msg1"].val2,
            self.test_types.val18["msg2"].val1,
            self.test_types.val18["msg2"].val2,
            self.test_types.val19[0].val1,
            self.test_types.val19[0].val2,
            self.test_types.val19[1].val1,
            self.test_types.val19[1].val2,
            self.test_types.val19[2].val1,
            self.test_types.val19[2].val2,
        ])))

    def test_flatten_mixed_protos_to_csv(self) -> None:
        stream = (
            self.raw_msg,
            self.n4,
            self.complex_msg,
            self.n6,
            self.n2,
            self.test_nested,
            self.test_specials,
            self.n3,
            self.test_types,
            self.n4_2,
            self.n4_3,
        )
        temp_dir = Path(tempfile.mkdtemp())
        flatten_mixed_proto_stream_to_csv(stream, temp_dir)

        # check all files exist
        created_files = [path.name for path in temp_dir.glob("*.csv")]
        for obj in stream:
            self.assertIn(f'{obj.DESCRIPTOR.full_name}.csv', created_files)

        # check N4
        self._check_n4_stream_to_csv(temp_dir / f'{self.n4.DESCRIPTOR.full_name}.csv')

    def test_flatten_same_protos_to_csv(self) -> None:
        stream = (
            self.n4,
            self.n4_2,
            self.n4_3,
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
                self.n4.id,
                self.n4.raw_msgs[0].id,
                self.n4.raw_msgs[0].timestamp,
                self.n4.raw_msgs[0].data,
                self.n4.raw_msgs[1].id,
                self.n4.raw_msgs[1].timestamp,
                self.n4.raw_msgs[1].data,
                self.n4.raw_msgs_by_id["msg0"].id,
                self.n4.raw_msgs_by_id["msg0"].timestamp,
                self.n4.raw_msgs_by_id["msg0"].data,
                self.n4.raw_msgs_by_id["msg1"].id,
                self.n4.raw_msgs_by_id["msg1"].timestamp,
                self.n4.raw_msgs_by_id["msg1"].data,
                '', '', '',
                '', '', '',
            ])))
            self.assertEqual(lines[2].rstrip('\n'), ','.join(map(str, [
                self.n4_2.id,
                self.n4_2.raw_msgs[0].id,
                self.n4_2.raw_msgs[0].timestamp,
                self.n4_2.raw_msgs[0].data,
                self.n4_2.raw_msgs[1].id,
                self.n4_2.raw_msgs[1].timestamp,
                self.n4_2.raw_msgs[1].data,
                self.n4_2.raw_msgs_by_id["msg0"].id,
                self.n4_2.raw_msgs_by_id["msg0"].timestamp,
                self.n4_2.raw_msgs_by_id["msg0"].data,
                '', '', '',
                self.n4_2.raw_msgs[2].id,
                self.n4_2.raw_msgs[2].timestamp,
                self.n4_2.raw_msgs[2].data,
                self.n4_2.raw_msgs_by_id["a"].id,
                self.n4_2.raw_msgs_by_id["a"].timestamp,
                self.n4_2.raw_msgs_by_id["a"].data,
            ])))
            self.assertEqual(lines[3].rstrip('\n'), ','.join(map(str, [
                self.n4_3.id,
                self.n4_3.raw_msgs[0].id,
                self.n4_3.raw_msgs[0].timestamp,
                self.n4_3.raw_msgs[0].data,
                self.n4_3.raw_msgs[1].id,
                self.n4_3.raw_msgs[1].timestamp,
                self.n4_3.raw_msgs[1].data,
                self.n4_3.raw_msgs_by_id["msg0"].id,
                self.n4_3.raw_msgs_by_id["msg0"].timestamp,
                self.n4_3.raw_msgs_by_id["msg0"].data,
                self.n4_3.raw_msgs_by_id["msg1"].id,
                self.n4_3.raw_msgs_by_id["msg1"].timestamp,
                self.n4_3.raw_msgs_by_id["msg1"].data,
                self.n4_3.raw_msgs[2].id,
                self.n4_3.raw_msgs[2].timestamp,
                self.n4_3.raw_msgs[2].data,
                self.n4_3.raw_msgs_by_id["a"].id,
                self.n4_3.raw_msgs_by_id["a"].timestamp,
                self.n4_3.raw_msgs_by_id["a"].data,
            ])))


if __name__ == "__main__":
    unittest.main()
