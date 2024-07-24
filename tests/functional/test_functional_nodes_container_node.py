"""This module contains functional tests for nodes ContainerNode."""

from yapyang.nodes import ContainerNode


class Interfaces(ContainerNode):
    """Represents a subclass of ContainerNode."""

    __identifier__: str = "interfaces"


def test_given_instance_of_container_node_subclass_when_to_xml_is_called_then_instance_xml_element_returned():
    """Test given instance of container node subclass when to xml is called then instance xml element returned."""

    # Given instance of ContainerNode subclass.

    # When to_xml is called.
    xml = Interfaces().to_xml()

    # Then instance XML element returned.
    assert xml == "<interfaces></interfaces>"


def test_given_instance_of_container_node_subclass_when_to_xml_is_called_with_attrs_then_instance_xml_element_with_attrs_returned():
    """Test given instance of container node subclass when to xml is called with attrs then instance xml element with attrs returned."""

    # Given instance of ContainerNode subclass.

    # When to_xml is called with attrs.
    xml = Interfaces().to_xml(attrs={"nc:operation": "delete"})

    # Then instance XML element with attrs returned.
    assert xml == '<interfaces nc:operation="delete"></interfaces>'


def test_given_instance_of_container_node_subclass_with_inner_nodes_when_to_xml_is_called_then_xml_tree_from_instance_xml_element_returned():
    """Test given instance of container node subclass with inner nodes when to xml is called then xml tree from instance xml element returned."""

    # Given instance of ContainerNode subclass with inner node.
    class System(ContainerNode):
        __identifier__: str = "system"

        interfaces: Interfaces

    # When to_xml is called.
    xml = System(Interfaces()).to_xml()

    # Then XML tree from instance XML element returned.
    assert xml == "<system><interfaces></interfaces></system>"
