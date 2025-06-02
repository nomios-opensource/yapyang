"""This module contains end-to-end tests for Union-typed fields and ListNode MetaInfo placeholders."""

import typing as t

import pytest

from yapyang import ContainerNode, LeafNode, ListNode, MetaInfo


@pytest.mark.parametrize(
    "interface_create, interface_delete, expected_xml",
    [
        (
            True,
            False,
            '<interface><name>demux0</name><unit operation="create"><name>1</name></unit></interface>',
        ),
        (
            False,
            True,
            '<interface><name>demux0</name><unit operation="delete"><name>2</name></unit></interface>',
        ),
        (
            True,
            True,
            '<interface><name>demux0</name><unit operation="create"><name>1</name></unit><unit operation="delete"><name>2</name></unit></interface>',
        ),
    ],
)
def test_given_configuration_elements_with_metainfo_placeholders_when_to_xml_is_called_then_xml_tree_returned(
    interface_create,
    interface_delete,
    expected_xml,
):
    """Test given configuration elements with MetaInfo placeholders when to_xml is called then xml tree returned."""

    # Given configuration elements with MetaInfo placeholders.
    class Name(LeafNode):
        __identifier__ = "name"

        value: str

    class Unit(ListNode):
        __identifier__ = "unit"
        __key__ = "name"

        name: Name

    class Interface(ListNode):
        __identifier__ = "interface"
        __key__ = "name"

        name: Name
        unit_create: Unit = MetaInfo(attrs={"operation": "create"})
        unit_delete: Unit = MetaInfo(attrs={"operation": "delete"})

    iface = Interface()
    uc_create = Unit()
    uc_delete = Unit()

    if interface_create:
        uc_create.append(name=Name("1"))
    if interface_delete:
        uc_delete.append(name=Name("2"))

    iface.append(
        name=Name("demux0"),
        unit_create=uc_create,
        unit_delete=uc_delete,
    )

    # When to_xml is called.

    # Then xml tree returned.
    assert iface.to_xml() == expected_xml


def test_given_configuration_elements_with_list_node_including_union_typed_attribute_when_to_xml_is_called_then_xml_tree_returned():
    """Test given configuration elements with list node including Union-typed attribute when to_xml is called then xml tree returned."""

    # Given configuration elements with list node including Union-typed attribute.
    class Name(LeafNode):
        __identifier__ = "name"

        value: str

    class IPv4(LeafNode):
        __identifier__ = "ipv4"

        value: str

    class Vlan(LeafNode):
        __identifier__ = "vlan"

        value: int

    class Interface(ListNode):
        __identifier__ = "interface"
        __key__ = "name"

        name: Name
        element: t.Union[IPv4, Vlan]

    iface_vlan = Interface()
    iface_vlan.append(Name("demux0"), Vlan(99))
    iface_ipv4 = Interface()
    iface_ipv4.append(Name("demux0"), IPv4("1.1.1.1"))

    # When to_xml is called.

    # Then xml tree returned.
    assert (
        iface_ipv4.to_xml()
        == "<interface><name>demux0</name><ipv4>1.1.1.1</ipv4></interface>"
    )
    assert (
        iface_vlan.to_xml()
        == "<interface><name>demux0</name><vlan>99</vlan></interface>"
    )


def test_given_configuration_elements_with_container_node_including_union_typed_attribute_when_to_xml_is_called_then_xml_tree_returned():
    """Test given configuration elements with container node including Union-typed attribute when to_xml is called then xml tree returned."""

    # Given configuration elements with container node including Union-typed attribute.
    class Interface(ContainerNode):
        __identifier__ = "interface"

    class SubInterface(ContainerNode):
        __identifier__ = "sub-interface"

    class Config(ContainerNode):
        __identifier__ = "config"
        __key__ = "name"

        element: t.Union[Interface, SubInterface]

    # When to_xml is called.

    # Then xml tree returned.
    assert (
        Config(SubInterface()).to_xml()
        == "<config><sub-interface></sub-interface></config>"
    )
    assert (
        Config(Interface()).to_xml()
        == "<config><interface></interface></config>"
    )
