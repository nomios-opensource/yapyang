"""This module contains end-to-end tests for Union-typed fields and ListNode MetaInfo placeholders."""

import typing as t
import pytest
from yapyang import ContainerNode, ListNode, LeafNode, MetaInfo


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
    unit_create: Unit = MetaInfo(attrs={"operation": "replace"})
    unit_delete: Unit = MetaInfo(attrs={"operation": "remove"})


class Foo(ContainerNode):
    __identifier__ = "foo"


class Bar(ContainerNode):
    __identifier__ = "bar"


class TestContainerUnion(ContainerNode):
    __identifier__ = "test-container-union"

    child: t.Union[Foo, Bar]


class TestListUnion(ListNode):
    __identifier__ = "test-list-union"
    __key__ = "name"

    name: Name
    child: t.Union[Foo, Bar]


def test_given_instance_of_container_node_subclass_with_union_typed_child_field_when_to_xml_is_called_then_only_selected_child_serialized():
    """Test given instance of ContainerNode subclass with Union-typed child field when to_xml is called then only selected child serialized."""

    # Given instance of ContainerNode subclass with Union-typed child field.

    # When to_xml is called.
    xml_foo = TestContainerUnion(Foo()).to_xml()
    xml_bar = TestContainerUnion(Bar()).to_xml()

    # Then only selected child serialized.
    assert (
        xml_foo == "<test-container-union><foo></foo></test-container-union>"
    )
    assert (
        xml_bar == "<test-container-union><bar></bar></test-container-union>"
    )


def test_given_instance_of_list_node_subclass_with_union_typed_child_field_when_to_xml_is_called_then_only_selected_child_serialized():
    """Test given instance of ListNode subclass with Union-typed child field when to_xml is called then only selected child serialized."""

    # Given instance of ListNode subclass with Union-typed child field.
    list_union_foo = TestListUnion()
    list_union_bar = TestListUnion()

    # When to_xml is called.
    list_union_foo.append(name=Name("a"), child=Foo())
    list_union_bar.append(name=Name("b"), child=Bar())
    xml_foo = list_union_foo.to_xml()
    xml_bar = list_union_bar.to_xml()

    # Then only selected child serialized.
    assert (
        xml_foo
        == "<test-list-union><name>a</name><foo></foo></test-list-union>"
    )
    assert (
        xml_bar
        == "<test-list-union><name>b</name><bar></bar></test-list-union>"
    )


@pytest.mark.parametrize(
    "create, delete, name_val, expected_xml",
    [
        (
            True,
            False,
            "one",
            "<interface>"
            "<name>one</name>"
            '<unit operation="replace"><name>one</name></unit>'
            "</interface>",
        ),
        (
            False,
            True,
            "two",
            "<interface>"
            "<name>two</name>"
            '<unit operation="remove"><name>two</name></unit>'
            "</interface>",
        ),
        (
            True,
            True,
            "three",
            "<interface>"
            "<name>three</name>"
            '<unit operation="replace"><name>three</name></unit>'
            '<unit operation="remove"><name>three</name></unit>'
            "</interface>",
        ),
    ],
)
def test_given_instance_of_list_node_subclass_with_metainfo_placeholders_when_to_xml_is_called_then_only_populated_branches_serialized(
    create, delete, name_val, expected_xml
):
    """Test given instance of ListNode subclass with MetaInfo placeholders when to_xml is called then only populated branches serialized."""

    # Given instance of ListNode subclass with MetaInfo placeholders.
    iface = Interface()
    uc_create = Unit()
    uc_delete = Unit()

    if create:
        uc_create.append(name=Name(name_val))
    if delete:
        uc_delete.append(name=Name(name_val))

    iface.append(
        name=Name(name_val),
        unit_create=uc_create,
        unit_delete=uc_delete,
    )

    # When to_xml is called.

    # Then only populated branches serialized.
    assert iface.to_xml() == expected_xml
