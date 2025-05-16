"""This module contains end-to-end tests for examples."""

from yapyang import *


def test_given_openconfig_interfaces_yang_model_when_nodes_instantiated_altered_and_to_xml_is_called_then_xml_tree_returned():
    """Test given openconfig interfaces yang model when nodes instantiated altered and to xml is called then xml tree returned."""

    # Given OpenConfig interfaces YANG model.
    class Name(LeafNode):
        __identifier__ = "name"

        value: str

    class Interface(ListNode):
        __identifier__ = "interface"
        __key__ = "name"

        name: Name

    class Interfaces(ContainerNode):
        __identifier__ = "interfaces"

        interface: Interface

    class OpenConfigInterfaces(ModuleNode):
        __identifier__ = "openconfig-interfaces"
        __namespace__ = "http://openconfig.net/yang/interfaces"

        interfaces: Interfaces

    # When nodes instantiated.
    module = OpenConfigInterfaces(Interfaces(Interface()))

    # When altered.
    module.interfaces.interface.append(Name("xe-0/0/0"))

    # When to_xml is called.
    xml = module.to_xml()

    # Then XML tree returned.
    assert (
        xml
        == '<interfaces xmlns="http://openconfig.net/yang/interfaces"><interface><name>xe-0/0/0</name></interface></interfaces>'
    )
