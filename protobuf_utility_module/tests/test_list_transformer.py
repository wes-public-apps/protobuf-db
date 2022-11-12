from unittest import TestCase
import unittest

import test_data as td

from protobuf_utility.transforms.list_transformer import flatten_proto_to_list


class TestListTransformer(TestCase):

    def test_flatten_proto_to_list_raw_msg(self) -> None:
        # Test Raw Msg
        attrs, values = flatten_proto_to_list(td.raw_msg)
        self.assertEqual(attrs, ["id", "timestamp", "data"])
        self.assertEqual(values, [td.raw_msg.id, td.raw_msg.timestamp, td.raw_msg.data])

    def test_flatten_proto_to_list_n4(self) -> None:
        # Test N4
        attrs, values = flatten_proto_to_list(td.n4)
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
        ])

    def test_flatten_proto_to_list_complex_message(self) -> None:
        # test complex
        attrs, values = flatten_proto_to_list(td.complex_msg)
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
            td.complex_msg.raw_msgs_by_id["msg0"].id,
            td.complex_msg.raw_msgs_by_id["msg0"].timestamp,
            td.complex_msg.raw_msgs_by_id["msg0"].data,
            td.complex_msg.raw_msgs_by_id["msg1"].id,
            td.complex_msg.raw_msgs_by_id["msg1"].timestamp,
            td.complex_msg.raw_msgs_by_id["msg1"].data,
            td.complex_msg.n4s[0].id,
            td.complex_msg.n4s[0].raw_msgs[0].id,
            td.complex_msg.n4s[0].raw_msgs[0].timestamp,
            td.complex_msg.n4s[0].raw_msgs[0].data,
            td.complex_msg.n4s[0].raw_msgs[1].id,
            td.complex_msg.n4s[0].raw_msgs[1].timestamp,
            td.complex_msg.n4s[0].raw_msgs[1].data,
            td.complex_msg.n4s[0].raw_msgs_by_id["msg0"].id,
            td.complex_msg.n4s[0].raw_msgs_by_id["msg0"].timestamp,
            td.complex_msg.n4s[0].raw_msgs_by_id["msg0"].data,
            td.complex_msg.n4s[0].raw_msgs_by_id["msg1"].id,
            td.complex_msg.n4s[0].raw_msgs_by_id["msg1"].timestamp,
            td.complex_msg.n4s[0].raw_msgs_by_id["msg1"].data,
            td.complex_msg.n4s[1].id,
            td.complex_msg.n4s[1].raw_msgs[0].id,
            td.complex_msg.n4s[1].raw_msgs[0].timestamp,
            td.complex_msg.n4s[1].raw_msgs[0].data,
            td.complex_msg.n4s[1].raw_msgs[1].id,
            td.complex_msg.n4s[1].raw_msgs[1].timestamp,
            td.complex_msg.n4s[1].raw_msgs[1].data,
            td.complex_msg.n4s[1].raw_msgs_by_id["msg0"].id,
            td.complex_msg.n4s[1].raw_msgs_by_id["msg0"].timestamp,
            td.complex_msg.n4s[1].raw_msgs_by_id["msg0"].data,
            td.complex_msg.n4s[1].raw_msgs_by_id["msg1"].id,
            td.complex_msg.n4s[1].raw_msgs_by_id["msg1"].timestamp,
            td.complex_msg.n4s[1].raw_msgs_by_id["msg1"].data,
            td.complex_msg.n4s_by_id["msg0"].id,
            td.complex_msg.n4s_by_id["msg0"].raw_msgs[0].id,
            td.complex_msg.n4s_by_id["msg0"].raw_msgs[0].timestamp,
            td.complex_msg.n4s_by_id["msg0"].raw_msgs[0].data,
            td.complex_msg.n4s_by_id["msg0"].raw_msgs[1].id,
            td.complex_msg.n4s_by_id["msg0"].raw_msgs[1].timestamp,
            td.complex_msg.n4s_by_id["msg0"].raw_msgs[1].data,
            td.complex_msg.n4s_by_id["msg0"].raw_msgs_by_id["msg0"].id,
            td.complex_msg.n4s_by_id["msg0"].raw_msgs_by_id["msg0"].timestamp,
            td.complex_msg.n4s_by_id["msg0"].raw_msgs_by_id["msg0"].data,
            td.complex_msg.n4s_by_id["msg0"].raw_msgs_by_id["msg1"].id,
            td.complex_msg.n4s_by_id["msg0"].raw_msgs_by_id["msg1"].timestamp,
            td.complex_msg.n4s_by_id["msg0"].raw_msgs_by_id["msg1"].data,
            td.complex_msg.n4s_by_id["msg1"].id,
            td.complex_msg.n4s_by_id["msg1"].raw_msgs[0].id,
            td.complex_msg.n4s_by_id["msg1"].raw_msgs[0].timestamp,
            td.complex_msg.n4s_by_id["msg1"].raw_msgs[0].data,
            td.complex_msg.n4s_by_id["msg1"].raw_msgs[1].id,
            td.complex_msg.n4s_by_id["msg1"].raw_msgs[1].timestamp,
            td.complex_msg.n4s_by_id["msg1"].raw_msgs[1].data,
            td.complex_msg.n4s_by_id["msg1"].raw_msgs_by_id["msg0"].id,
            td.complex_msg.n4s_by_id["msg1"].raw_msgs_by_id["msg0"].timestamp,
            td.complex_msg.n4s_by_id["msg1"].raw_msgs_by_id["msg0"].data,
            td.complex_msg.n4s_by_id["msg1"].raw_msgs_by_id["msg1"].id,
            td.complex_msg.n4s_by_id["msg1"].raw_msgs_by_id["msg1"].timestamp,
            td.complex_msg.n4s_by_id["msg1"].raw_msgs_by_id["msg1"].data,
            td.complex_msg.n5s_by_id["msg0"].types[0],
            td.complex_msg.n5s_by_id["msg0"].types[1],
            td.complex_msg.n5s_by_id["msg0"].data,
            td.complex_msg.n5s_by_id["msg1"].types[0],
            td.complex_msg.n5s_by_id["msg1"].types[1],
            td.complex_msg.n5s_by_id["msg1"].data,
        ])

    def test_flatten_proto_to_list_n6(self) -> None:
        # test n6
        attrs, values = flatten_proto_to_list(td.n6)
        self.assertEqual(attrs, [
            'n5val.data',
        ])
        self.assertEqual(values, [
            td.n6.n5val.data,
        ])

    def test_flatten_proto_to_list_n2(self) -> None:
        # test n2
        attrs, values = flatten_proto_to_list(td.n2)
        self.assertEqual(attrs, [
            'val2',
        ])
        self.assertEqual(values, [
            td.n2.val2,
        ])

    def test_flatten_proto_to_list_nested(self) -> None:
        # test nested
        attrs, values = flatten_proto_to_list(td.test_nested)
        self.assertEqual(attrs, [
            'val1.val1',
            'val2.val2',
        ])
        self.assertEqual(values, [
            td.test_nested.val1.val1,
            td.test_nested.val2.val2,
        ])

    def test_flatten_proto_to_list_specials(self) -> None:
        # test specials
        # dictionaries keys are sorted alphabetically
        attrs, values = flatten_proto_to_list(td.test_specials)
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
            td.test_specials.list1[0],
            td.test_specials.list1[1],
            td.test_specials.list1[2],
            td.test_specials.map1["key1"],
            td.test_specials.map1["key2"],
            td.test_specials.map1["key3"],
            td.test_specials.fault1,
            td.test_specials.fault2,
        ])

    def test_flatten_proto_to_list_n3(self) -> None:
        # test N3
        attrs, values = flatten_proto_to_list(td.n3)
        self.assertEqual(attrs, [
            'val1',
            'val2',
        ])
        self.assertEqual(values, [
            td.n3.val1,
            td.n3.val2,
        ])

    def test_flatten_proto_to_list_types(self) -> None:
        # test types
        attrs, values = flatten_proto_to_list(td.test_types)
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
            td.test_types.val15,
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
        ])

        # Handled changing the location of a field in the protobuf but keep the id.
        # TODO(wesley): add test case


if __name__ == "__main__":
    unittest.main()
