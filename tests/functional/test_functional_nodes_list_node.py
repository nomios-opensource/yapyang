"""This module contains functional tests for nodes ListNode."""

from yapyang.nodes import ListNode, LeafNode
from yapyang.utils import MetaInfo


class Name(LeafNode):
    """Represents a ListNode child node."""

    __identifier__: str = "name"

    value: str


class Interface(ListNode):
    """Represents a subclass of ListNode."""

    __identifier__: str = "interface"
    __key__: str = "name"

    name: Name


def test_given_instance_of_list_node_subclass_with_entries_when_to_xml_is_called_then_xml_tree_from_each_entry_xml_element_returned():
    """Test given instance of list node subclass with entries when to xml is called then xml tree from each entry xml element returned."""

    # Given instance of ListNode subclass with entries.
    interface = Interface()
    interface.append(Name("et-0/0/0"))
    interface.append(Name("xe-0/0/1"))

    # When to_xml is called.
    xml = interface.to_xml()

    # Then XML tree from each entry XML element returned.
    assert (
        xml
        == "<interface><name>et-0/0/0</name></interface><interface><name>xe-0/0/1</name></interface>"
    )


def test_given_instance_of_list_node_subclass_with_entries_when_to_xml_is_called_with_attrs_then_xml_tree_from_each_entry_xml_element_with_attrs_returned():
    """Test given instance of list node subclass with entries when to xml is called with attrs then xml tree from each entry xml element with attrs returned."""

    # Given instance of ListNode subclass with entries.
    interface = Interface()
    interface.append(Name("et-0/0/0"))
    interface.append(Name("xe-0/0/1"))

    # When to_xml is called with attrs.
    xml = interface.to_xml(attrs={"nc:operation": "delete"})

    # Then XML tree from each entry XML element with attrs returned.
    assert (
        xml
        == '<interface nc:operation="delete"><name>et-0/0/0</name></interface><interface nc:operation="delete"><name>xe-0/0/1</name></interface>'
    )


def test_given_instance_of_list_node_subclass_with_child_nodes_given_child_nodes_have_meta_info_default_with_attrs_when_to_xml_is_called_then_entries_child_node_xml_elements_contain_attrs():
    """Test given instance of list node subclass with child nodes given child nodes have meta info default with attrs when to xml is called then entries child node xml elements contain attrs."""

    # Given instance of list node subclass with child node.
    # Given child node have MetaInfo default with attrs.
    class InterfaceDefaultMeta(Interface):
        """Represents a subclass of ListNode."""

        name: Name = MetaInfo(attrs={"nc:operation": "delete"})

    interface = InterfaceDefaultMeta()
    interface.append(Name("xe-0/0/0"))

    # When to_xml is called.
    xml = interface.to_xml()

    # Then entries child node XML element contain attrs.
    assert (
        xml
        == '<interface><name nc:operation="delete">xe-0/0/0</name></interface>'
    )


def test_given_instance_of_list_node_subclass_with_child_nodes_given_child_nodes_have_meta_info_default_without_attrs_when_to_xml_is_called_then_xml_tree_from_each_entry_xml_element_returned():
    """Test given instance of list node subclass with child nodes given child nodes have meta info default without attrs when to xml is called then xml tree from each entry xml element returned."""

    # Given instance of list node subclass with child node.
    # Given child node have MetaInfo default without attrs.
    class InterfaceDefaultMeta(Interface):
        """Represents a subclass of ListNode."""

        name: Name = MetaInfo()

    interface = InterfaceDefaultMeta()
    interface.append(Name("xe-0/0/0"))

    # When to_xml is called.
    xml = interface.to_xml()

    # Then XML tree from each entry XML element returned.
    assert xml == "<interface><name>xe-0/0/0</name></interface>"
