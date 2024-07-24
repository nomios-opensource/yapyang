"""This module contains functional tests for nodes ListNode."""

import pytest
from ordered_set import OrderedSet

from yapyang.nodes import ListNode, LeafNode


class Name(LeafNode):
    """Represents a ListNode inner node."""

    __identifier__: str = "name"

    value: str


DEFAULT = Name("xe-0/0/0")


class Interface(ListNode):
    """Represents a subclass of ListNode."""

    __identifier__: str = "interface"
    __key__: str = "name"

    name: Name = DEFAULT


def test_given_subclass_of_list_node_when_instantiated_then_entries_attribute_created():
    """Test given subclass of list node when instantiated then entries attribute created."""

    # Given subclass of ListNode.

    # When instantiated.
    mock_list = Interface()

    # Then entries attribute created.
    assert "entries" in mock_list.__dict__
    assert isinstance(mock_list.entries, OrderedSet)


def test_given_instance_of_list_node_subclass_when_append_is_called_with_args_then_args_are_assigned_in_order_of_annotated_cls_attributes_and_entry_is_created_in_entries():
    """Test given instance of list node subclass when append is called with args then args are assigned in order of annotated cls attributes and entry is created in entries."""

    # Given instance of ListNode subclass.
    mock_list = Interface()
    name = Name("xe-0/0/1")

    # When append is called with args.
    mock_list.append(name)

    # Then args are assigned in order of annotated cls attributes
    # and entry is created in entries.
    assert mock_list.entries[0].name is name


def test_given_instance_of_list_node_subclass_when_append_is_called_with_kwargs_then_kwargs_are_assigned_for_annotated_cls_attributes_and_entry_is_created_in_entries():
    """Test given instance of list node subclass when append is called with kwargs then kwargs are assigned for annotated cls attributes and entry is created in entries."""

    # Given instance of ListNode subclass.
    mock_list = Interface()
    name = Name("xe-0/0/1")

    # When append is called with kwargs.
    mock_list.append(name=name)

    # Then kwargs are assigned for annotated cls attributes and entry
    # is created in entries.
    assert mock_list.entries[0].name is name


def test_given_instance_of_list_node_subclass_when_append_is_called_without_args_or_kwargs_then_defaults_are_assigned_for_annotated_cls_attributes_and_entry_is_created_in_entries():
    """Test given instance of list node subclass when append is called without args or kwargs then defaults are assigned for annotated cls attributes and entry is created in entries."""

    # Given instance of ListNode subclass.
    mock_list = Interface()

    # When append is called without args or kwargs.
    mock_list.append()

    # Then defaults are assigned for annotated cls attributes and
    # entry is created in entries.
    assert mock_list.entries[0].name is DEFAULT


def test_given_instance_of_list_node_subclass_when_append_is_called_with_too_many_args_or_kwargs_then_exception_is_raised():
    """Test given instance of list node subclass when append is called with too many args or kwargs then exception is raised."""

    # Given instance of ListNode subclass.
    mock_list = Interface()

    # When append is called with too many args.
    with pytest.raises(TypeError) as exc:
        mock_list.append("junos", "Too Many!")

    # Then exception has expected message.
    assert (
        str(exc.value)
        == f"{Interface.__name__} takes 1 arguments, but 2 were given."
    )


def test_given_instance_of_list_node_subclass_when_append_is_called_with_too_few_args_or_kwargs_then_exception_is_raised():
    """Test given instance of list node subclass when append is called with too few args or kwargs then exception is raised."""

    # Given instance of ListNode subclass.
    class System(ListNode):
        """Represents a subclass of ListNode."""

        __identifier__: str = "system"
        __key__: str = "interfaces"

        interfaces: Interface

    # When append is called with too few args.
    with pytest.raises(TypeError) as exc:
        System().append()

    # Then exception has expected message.
    assert str(exc.value) == "Missing required argument: interfaces"


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
