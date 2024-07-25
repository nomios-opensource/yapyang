"""This module contains functional tests for nodes ModuleNode."""

from yapyang.nodes import ContainerNode, ModuleNode
from yapyang.utils import MetaInfo


class JunosInterfaces(ContainerNode):
    """Represents a ModuleNode child node."""

    __identifier__: str = "interfaces"


class JunosEsConfInterfaces(ModuleNode):
    """Represents a subclass of ModuleNode"""

    __identifier__: str = "junos-es-conf-interfaces"
    __namespace__: str = "http://yang.juniper.net/junos-es/conf/interfaces"

    interfaces: JunosInterfaces = JunosInterfaces()


def test_given_instance_of_module_node_subclass_with_child_nodes_when_to_xml_is_called_then_xml_tree_from_instance_returned():
    """Test given instance of module node subclass with child nodes when to xml is called then xml tree from instance returned."""

    # Given instance of ModuleNode subclass with child nodes.

    # When to_xml is called.
    xml = JunosEsConfInterfaces().to_xml()

    # Then XML tree from instance returned.
    assert (
        xml
        == '<interfaces xmlns="http://yang.juniper.net/junos-es/conf/interfaces"></interfaces>'
    )


def test_given_instance_of_module_node_subclass_with_child_nodes_given_child_nodes_have_meta_info_default_with_attrs_when_to_xml_is_called_then_child_node_xml_elements_contain_attrs():
    """Test given instance of module node subclass with child nodes given child nodes have meta info default with attrs when to xml is called then child node xml elements contain attrs."""

    # Given instance of ModuleNode subclass with child nodes.
    # Given child nodes have MetaInfo default with attrs.
    class Override(JunosEsConfInterfaces):
        """Represents a subclass of ModuleNode."""

        interfaces: JunosInterfaces = MetaInfo(
            attrs={"nc:operation": "create"}
        )

    # When to_xml is called.
    xml = Override(JunosInterfaces()).to_xml()

    # Then child node XML element contain attrs.
    assert (
        xml
        == '<interfaces xmlns="http://yang.juniper.net/junos-es/conf/interfaces" nc:operation="create"></interfaces>'
    )


def test_given_instance_of_module_node_subclass_with_child_nodes_given_child_nodes_have_meta_info_default_without_attrs_when_to_xml_is_called_then_xml_tree_from_instance_returned():
    """Test given instance of module node subclass with child nodes given child nodes have meta info default without attrs when to xml is called then xml tree from instance returned."""

    # Given instance of ModuleNode subclass with child nodes.
    # Given child nodes have MetaInfo default without attrs.
    class Override(JunosEsConfInterfaces):
        """Represents a subclass of ModuleNode."""

        interfaces: JunosInterfaces = MetaInfo()

    # When to_xml is called.
    xml = Override(JunosInterfaces()).to_xml()

    # Then XML tree from instance returned.
    assert (
        xml
        == '<interfaces xmlns="http://yang.juniper.net/junos-es/conf/interfaces"></interfaces>'
    )
