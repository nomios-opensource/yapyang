"""This module contains functional tests for nodes ModuleNode."""

from yapyang.nodes import ContainerNode, ModuleNode


class JunosInterfaces(ContainerNode):
    """Represents a ModuleNode inner node."""

    __identifier__: str = "interfaces"


class JunosEsConfInterfaces(ModuleNode):
    """Represents a subclass of ModuleNode"""

    __identifier__: str = "junos-es-conf-interfaces"
    __namespace__: str = "http://yang.juniper.net/junos-es/conf/interfaces"

    interfaces: JunosInterfaces


def test_given_instance_of_module_node_subclass_with_inner_nodes_when_to_xml_is_called_then_xml_tree_from_instance_returned():
    """Test given instance of module node subclass with inner nodes when to xml is called then xml tree from instance returned."""

    # Give instance of ModuleNode subclass with inner nodes.

    # When to_xml is called.
    xml = JunosEsConfInterfaces(JunosInterfaces()).to_xml()

    # Then XML tree from instance returned.
    assert (
        xml
        == '<interfaces xmlns="http://yang.juniper.net/junos-es/conf/interfaces"></interfaces>'
    )
