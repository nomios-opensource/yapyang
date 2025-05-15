"""This module contains functional tests for nodes ContainerNode."""

import typing as t
from yapyang.nodes import ContainerNode
from yapyang.utils import MetaInfo


class Interfaces(ContainerNode):
    """Represents a subclass of ContainerNode."""

    __identifier__: str = "interfaces"


class Vlan(ContainerNode):
    """Represents a subclass of ContainerNode."""

    __identifier__: str = "vlan"


class System(ContainerNode):
    """Represents a subclass of ContainerNode."""

    __identifier__: str = "system"

    interfaces: Interfaces = Interfaces()


class TestUnion(ContainerNode):
    """Represents a subclass of ContainerNode with a Union-typed child field."""

    __identifier__: str = "test-union"

    union_field: t.Union[Interfaces, Vlan]


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


def test_given_instance_of_container_node_subclass_with_child_nodes_when_to_xml_is_called_then_xml_tree_from_instance_xml_element_returned():
    """Test given instance of container node subclass with child nodes when to xml is called then xml tree from instance xml element returned."""

    # Given instance of ContainerNode subclass with child node.

    # When to_xml is called.
    xml = System().to_xml()

    # Then XML tree from instance XML element returned.
    assert xml == "<system><interfaces></interfaces></system>"


def test_given_instance_of_container_node_subclass_with_child_nodes_given_child_nodes_have_meta_info_default_with_attrs_when_to_xml_is_called_then_child_node_xml_elements_contain_attrs():
    """Test given instance of container node subclass with child nodes given child nodes have meta info default with attrs when to xml is called then child node xml elements contain attrs."""

    # Given instance of ContainerNode subclass with child nodes.
    # Given child nodes have MetaInfo default with attrs.
    class Override(System):
        """Represents a subclass of ContainerNode."""

        interfaces: Interfaces = MetaInfo(attrs={"nc:operation": "delete"})

    # When to_xml is called.
    xml = Override(Interfaces()).to_xml()

    # Then child node XML element contain attrs.
    assert (
        xml
        == '<system><interfaces nc:operation="delete"></interfaces></system>'
    )


def test_given_instance_of_container_node_subclass_with_child_nodes_given_child_nodes_have_meta_info_default_without_attrs_when_to_xml_is_called_then_xml_tree_from_instance_xml_element_returned():
    """Test given instance of container node subclass with child nodes given child nodes have meta info default without attrs when to xml is called then xml tree from instance xml element returned."""

    # Given instance of ContainerNode subclass with child nodes.
    # Given child nodes have MetaInfo default without attrs.
    class Override(System):
        """Represents a subclass of ContainerNode."""

        interfaces: Interfaces = MetaInfo()

    # When to_xml is called.
    xml = Override(Interfaces()).to_xml()

    # Then XML tree from instance XML element returned.
    assert xml == "<system><interfaces></interfaces></system>"


def test_given_instance_of_container_node_subclass_with_union_typed_child_field_when_to_xml_is_called_then_only_selected_child_serialized():
    """Test given instance of container node subclass with Union-typed child field when to xml is called then only selected child serialized."""

    # Given instance of ContainerNode subclass with child nodes.

    # When to_xml is called.
    xml_if = TestUnion(Interfaces()).to_xml()
    xml_vlan = TestUnion(Vlan()).to_xml()

    # Then only selected child serialized.
    assert xml_if == "<test-union><interfaces></interfaces></test-union>"
    assert xml_vlan == "<test-union><vlan></vlan></test-union>"
