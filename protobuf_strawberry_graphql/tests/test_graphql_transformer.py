from unittest import TestCase
import unittest

from protobuf_strawberry_graphql import definition_to_query

from complex_pb2 import ComplexMessage


class TestGraphqlTransformer(TestCase):

    def test_proto_definition_to_graphql_raw(self) -> None:
        pass

    def test_proto_definition_to_graphql_n4(self) -> None:
        pass

    def test_proto_definition_to_graphql_complex(self) -> None:
        print(definition_to_query(ComplexMessage), flush=True)

    def test_proto_definition_to_graphql_n6(self) -> None:
        pass

    def test_proto_definition_to_graphql_n2(self) -> None:
        pass

    def test_proto_definition_to_graphql_nested(self) -> None:
        pass

    def test_proto_definition_to_graphql_specials(self) -> None:
        pass

    def test_proto_definition_to_graphql_n3(self) -> None:
        pass

    def test_proto_definition_to_graphql_types(self) -> None:
        pass


if __name__ == "__main__":
    unittest.main()
