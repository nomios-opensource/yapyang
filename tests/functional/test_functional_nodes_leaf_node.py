"""This module contains functional tests for nodes LeafNode."""

from yapyang.nodes import LeafNode


class Name(LeafNode):
    """Represents a subclass of LeafNode."""

    __identifier__: str = "name"

    value: str


def test_given_instance_of_leaf_node_subclass_when_to_xml_is_called_then_instance_xml_element_returned():
    """Test given instance of leaf node subclass when to xml is called then instance xml element returned."""

    # Given instance of LeafNode subclass.

    # When to_xml is called.
    xml = Name("xe-0/0/0").to_xml()

    # Then instance XML element returned.
    assert xml == "<name>xe-0/0/0</name>"


def test_given_instance_of_leaf_node_subclass_when_to_xml_is_called_with_attrs_then_instance_xml_element_with_attrs_returned():
    """Test given instance of leaf node subclass when to xml is called with attrs then instance xml element with attrs returned."""

    # Given instance of LeafNode subclass.

    # When to_xml is called with attrs.
    xml = Name("xe-0/0/0").to_xml(attrs={"nc:operation": "delete"})

    # Then instance XML element with attrs returned.
    assert xml == '<name nc:operation="delete">xe-0/0/0</name>'
