import logging
from unittest import TestCase
import unittest

from common_pb2 import RawMsg
from complex_pb2 import N4, N6, ComplexMessage
from nested_pb2 import N2, TestNested
from specials_pb2 import TestSpecials
import test_data as td
from types_pb2 import N3, TestTypes, TYPES

from protobuf_utility.transforms.graphql_transformer import (
    proto_definition_to_graphql_query,
    proto_definition_to_strawberry_types,
    proto_descriptor_to_strawberry_type
)

logging.getLogger().setLevel(logging.DEBUG)


class TestGraphqlTransformer(TestCase):

    # region Test GraphQL Schema Generation using Strawberry
    def test_proto_definition_to_graphql_schema_strawberry_complex(self) -> None:
        print()
        for type_, file in proto_definition_to_strawberry_types(ComplexMessage).items():
            print(type_, file)

    def test_proto_definition_to_strawberry_type_raw(self) -> None:
        from queue import Queue
        imports = set()
        print(
            proto_descriptor_to_strawberry_type(RawMsg.DESCRIPTOR, imports, Queue())
        )
        print(imports)

    def test_proto_definition_to_strawberry_type_complex(self) -> None:
        from queue import Queue
        imports = set()
        print(
            proto_descriptor_to_strawberry_type(ComplexMessage.DESCRIPTOR, imports, Queue())
        )
        print(imports)

    def test_proto_definition_to_strawberry_type_types(self) -> None:
        from queue import Queue
        imports = set()
        print(
            proto_descriptor_to_strawberry_type(TestTypes.DESCRIPTOR, imports, Queue())
        )
        print(imports)
    # endregion

    # region Test GraphQL Query Generation
    def test_proto_definition_to_graphql_query_raw(self) -> None:
        self.assertEqual(
            proto_definition_to_graphql_query(td.raw_msg),
            '{\n\tid\n\ttimestamp\n\tdata\n}'
        )

    def test_proto_definition_to_graphql_query_n4(self) -> None:
        self.assertEqual(
            proto_definition_to_graphql_query(td.n4),
            '{\n\tid\n\traw_msgs {\n\t\tid\n\t\ttimestamp\n\t\tdata\n\t}\n\traw_msgs_by_id {\n\t\tkey\n\t\tvalue {\n\t\t\tid\n\t\t\ttimestamp\n\t\t\tdata\n\t\t}\n\t}\n}'
        )

    def test_proto_definition_to_graphql_query_complex(self) -> None:
        self.assertEqual(
            proto_definition_to_graphql_query(td.complex_msg),
            '{\n\traw_msgs_by_id {\n\t\tkey\n\t\tvalue {\n\t\t\tid\n\t\t\ttimestamp\n\t\t\tdata\n\t\t}\n\t}\n\tn4s {\n\t\tid\n\t\traw_msgs {\n\t\t\tid\n\t\t\ttimestamp\n\t\t\tdata\n\t\t}\n\t\traw_msgs_by_id {\n\t\t\tkey\n\t\t\tvalue {\n\t\t\t\tid\n\t\t\t\ttimestamp\n\t\t\t\tdata\n\t\t\t}\n\t\t}\n\t}\n\tn4s_by_id {\n\t\tkey\n\t\tvalue {\n\t\t\tid\n\t\t\traw_msgs {\n\t\t\t\tid\n\t\t\t\ttimestamp\n\t\t\t\tdata\n\t\t\t}\n\t\t\traw_msgs_by_id {\n\t\t\t\tkey\n\t\t\t\tvalue {\n\t\t\t\t\tid\n\t\t\t\t\ttimestamp\n\t\t\t\t\tdata\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t}\n\tn5s_by_id {\n\t\tkey\n\t\tvalue {\n\t\t\ttypes\n\t\t\tdata\n\t\t}\n\t}\n}'
        )

    def test_proto_definition_to_graphql_query_n6(self) -> None:
        self.assertEqual(
            proto_definition_to_graphql_query(td.n6),
            '{\n\tn5val {\n\t\ttypes\n\t\tdata\n\t}\n}'
        )

    def test_proto_definition_to_graphql_query_n2(self) -> None:
        self.assertEqual(
            proto_definition_to_graphql_query(td.n2),
            '{\n\tval2\n}'
        )

    def test_proto_definition_to_graphql_query_nested(self) -> None:
        self.assertEqual(
            proto_definition_to_graphql_query(td.test_nested),
            '{\n\tval1 {\n\t\tval1\n\t}\n\tval2 {\n\t\tval2\n\t}\n}'
        )

    def test_proto_definition_to_graphql_query_specials(self) -> None:
        self.assertEqual(
            proto_definition_to_graphql_query(td.test_specials),
            '{\n\tlist1\n\tmap1 {\n\t\tkey\n\t\tvalue\n\t}\n\tfault1\n\tfault2\n}'
        )

    def test_proto_definition_to_graphql_query_n3(self) -> None:
        self.assertEqual(
            proto_definition_to_graphql_query(td.n3),
            '{\n\tval1\n\tval2\n}'
        )

    def test_proto_definition_to_graphql_query_types(self) -> None:
        self.assertEqual(
            proto_definition_to_graphql_query(td.test_types),
            '{\n\tval1\n\tval2\n\tval3\n\tval4\n\tval5\n\tval6\n\tval7\n\tval8\n\tval9\n\tval10\n\tval11\n\tval12\n\tval13\n\tval14\n\tval15\n\tval16\n\tval17 {\n\t\tval1\n\t\tval2\n\t}\n\tval18 {\n\t\tkey\n\t\tvalue {\n\t\t\tval1\n\t\t\tval2\n\t\t}\n\t}\n\tval19 {\n\t\tval1\n\t\tval2\n\t}\n}'
        )
    # endregion


if __name__ == "__main__":
    unittest.main()
