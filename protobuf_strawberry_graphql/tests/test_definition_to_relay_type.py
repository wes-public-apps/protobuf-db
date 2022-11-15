from unittest import TestCase
import unittest

from protobuf_strawberry_graphql import create_definition_tree, definition_tree_to_relay_type

from complex_pb2 import ComplexMessage


class TestDefinitionToRelayType(TestCase):

    def test_raw(self) -> None:
        self.assertTrue(False)

    def test_n4(self) -> None:
        self.assertTrue(False)

    def test_complex(self) -> None:
        tree = create_definition_tree(ComplexMessage)
        print(definition_tree_to_relay_type(tree), flush=True)
        self.assertTrue(False)

    def test_n6(self) -> None:
        self.assertTrue(False)

    def test_n2(self) -> None:
        self.assertTrue(False)

    def test_nested(self) -> None:
        self.assertTrue(False)

    def test_specials(self) -> None:
        self.assertTrue(False)

    def test_n3(self) -> None:
        self.assertTrue(False)

    def test_types(self) -> None:
        self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()
