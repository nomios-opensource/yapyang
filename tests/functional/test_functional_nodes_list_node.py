"""This module contains functional tests for list node."""

import pytest
from ordered_set import OrderedSet

from yapyang.nodes import ListNode


class MockListNode(ListNode):
    """Represents subclass of ListNode."""

    key: str = "name"
    name: str = "cisco"


def test_given_subclass_of_list_node_when_instantiated_then_entries_attribute_created():
    """Test given subclass of list node when instantiated then entries attribute created."""

    # Given MockListNode subclass of ListNode.

    # When MockListNode instantiated.
    mock_list = MockListNode()

    # Then entries attribute created.
    assert "entries" in mock_list.__dict__
    assert isinstance(mock_list.entries, OrderedSet)


def test_given_instance_of_subclass_of_list_node_when_append_is_called_with_args_then_args_are_assigned_in_order_of_annotated_cls_attributes_and_entry_is_created_in_entries():
    """Test given instance of subclass of list node when append is called with args then args are assigned in order of annotated cls attributes and entry is created in entries."""

    # Given instance of MockListNode subclass of ListNode.
    mock_list = MockListNode()
    name = "junos"

    # When append is called with args.
    mock_list.append(name)

    # Then args are assigned in order of annotated cls attributes
    # and entry is created in entries.
    assert mock_list.entries[0].name is name


def test_given_instance_of_subclass_of_list_node_when_append_is_called_with_kwargs_then_kwargs_are_assigned_for_annotated_cls_attributes_and_entry_is_created_in_entries():
    """Test given instance of subclass of list node when append is called with kwargs then kwargs are assigned for annotated cls attributes and entry is created in entries."""

    # Given instance of MockListNode subclass of ListNode.
    mock_list = MockListNode()
    name = "junos"

    # When append is called with kwargs.
    mock_list.append(name=name)

    # Then kwargs are assigned for annotated cls attributes and entry
    # is created in entries.
    assert mock_list.entries[0].name is name


def test_given_instance_of_subclass_of_list_node_when_append_is_called_without_args_or_kwargs_then_defaults_are_assigned_for_annotated_cls_attributes_and_entry_is_created_in_entries():
    """Test given instance of subclass of list node when append is called without args or kwargs then defaults are assigned for annotated cls attributes and entry is created in entries."""

    # Given instance of MockListNode subclass of ListNode.
    mock_list = MockListNode()

    # When append is called without args or kwargs.
    mock_list.append()

    # Then defaults are assigned for annotated cls attributes and
    # entry is created in entries.
    assert mock_list.entries[0].name == "cisco"


def test_given_instance_of_subclass_of_list_node_when_append_is_called_with_too_many_args_or_kwargs_then_exception_is_raised():
    """Test given instance of subclass of list node when append is called with too many args or kwargs then exception is raised."""

    # Given instance of MockListNode subclass of ListNode.
    mock_list = MockListNode()

    # When append is called with too many args.
    with pytest.raises(TypeError) as exc:
        mock_list.append("junos", "Too Many!")

    # Then exception has expected message.
    assert (
        str(exc.value)
        == f"{MockListNode.__name__} takes 1 arguments, but 2 were given."
    )


def test_given_instance_of_subclass_of_list_node_when_append_is_called_with_too_few_args_or_kwargs_then_exception_is_raised():
    """Test given instance of subclass of list node when append is called with too few args or kwargs then exception is raised."""

    # Given instance of ExtraMockListNode subclass of MockListNode.
    class ExtraMockListNode(MockListNode):
        status: str

    mock_list = ExtraMockListNode()

    # When append is called with too few args.
    with pytest.raises(TypeError) as exc:
        mock_list.append("Too Few!")

    # Then exception has expected message.
    assert str(exc.value) == "Missing required argument: status"
