"""This module contains end-to-end tests for the XML functionality of nodes."""

from yapyang.nodes import LeafNode, ListNode, ContainerNode, ModuleNode


def test_given_instance_of_module_node_with_container_list_and_leaf_nodes_when_to_xml_is_called_then_expected_xml_returned():
    """Test given instance of module node with container, list, and leaf nodes when to xml is called then expected xml returned."""

    # Given an instance of a ModuleNode subclass with container, list, and leaf nodes.
    class Name(LeafNode):
        """Represents a subclass of LeafNode."""

        __identifier__ = "name"

        value: str

    class Interface(ListNode):
        """Represents a subclass of ListNode."""

        __identifier__ = "interface"
        __key__ = "name"

        name: Name

    class Interfaces(ContainerNode):
        """Represents a subclass of ContainerNode."""

        __identifier__ = "interfaces"

        interface: Interface

    class OpenConfigInterfaces(ModuleNode):
        """Represents a subclass of ModuleNode."""

        __identifier__ = "openconfig-interfaces"
        __namespace__ = "http://openconfig.net/yang/interfaces"

        interfaces: Interfaces

    module = OpenConfigInterfaces(Interfaces(Interface()))
    module.interfaces.interface.append(Name("xe-0/0/0"))

    # When to_xml is called.
    xml = module.to_xml()

    # Then the expected XML is returned.
    expected_xml = '<interfaces xmlns="http://openconfig.net/yang/interfaces"><interface><name>xe-0/0/0</name></interface></interfaces>'
    assert xml == expected_xml
