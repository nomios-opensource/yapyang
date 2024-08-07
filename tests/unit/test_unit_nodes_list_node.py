"""This module contains unit tests for nodes ListNode."""

import random
import string
from unittest.mock import MagicMock, patch

import pytest
from ordered_set import OrderedSet

from yapyang.nodes import LeafNode, ListEntry, ListNode, Node


class FirstOrLastName(LeafNode):
    """Represents a ListNode child node."""

    value: str


class MockListNode(ListNode):
    """Represents a subclass of ListNode."""

    __key__: str = "firstname"

    firstname: FirstOrLastName
    lastname: FirstOrLastName


def test_given_list_node_subclass_when_instantiated_then_entries_attribute_created():
    """Test given list node subclass when instantiated then entries attribute created."""

    # Given ListNode subclass.

    # When instantiated.
    interface = MockListNode()

    # Then entries attribute created.
    assert "entries" in interface.__dict__
    assert isinstance(interface.entries, OrderedSet)


@patch.object(Node, "__init__")
def test_given_list_node_subclass_when_instantiated_then_node_initializer_called(
    node_init,
):
    """Test given list node subclass when instantiated then node initializer called."""

    # Given ListNode subclass.

    # When instantiated.
    with pytest.raises(AttributeError):
        # Then exception is raised for attributes that Node __init__
        # Mock did not create.
        MockListNode()

    # Then Node __init__ Mock was called.
    node_init.assert_called()


def test_given_instance_of_list_node_subclass_when_append_is_called_with_args_and_kwargs_then_cls_meta_args_resolver_yielded_cls_arg_value_pairs_are_set_as_attributes_of_new_list_entry():
    """Test given instance of list node subclass when append is called with args and kwargs then cls meta args resolver yielded cls arg value pairs are set as attributes of new list entry."""

    # Given args and kwargs.
    args = (1, 2, 3, 4, 5)
    kwargs = {"one": 1, "two": 2}

    # Given tuple of cls_arg, value pairs.
    cls_arg_value_pairs = tuple(
        (cls_arg, FirstOrLastName(random.choice(string.ascii_letters)))
        for cls_arg in MockListNode.__meta__["__args__"]
    )

    # Given Mock iterator with __iter__ method that returns a tuple
    # containing cls_arg, value pairs.
    mock_iterator = MagicMock()
    mock_iterator.__iter__.return_value = cls_arg_value_pairs

    # Given Mock _cls_meta_args_resolver that returns Mock iterator
    # when called.
    mock = MagicMock(return_value=mock_iterator)
    MockListNode._cls_meta_args_resolver = mock

    # Given instance of ListNode subclass.
    instance = MockListNode()

    # When append is called with args and kwargs.
    instance.append(*args, **kwargs)

    # Then Mock _cls_meta_args_resolver was called with args and kwargs.
    MockListNode._cls_meta_args_resolver.assert_called_once_with(args, kwargs)

    # Then Mock iterator __iter__ was called.
    mock_iterator.__iter__.assert_called()

    # Then new entry in entries.
    (entry,) = instance.entries
    assert isinstance(entry, ListEntry)

    # Then cls_arg, value pairs are set as attributes of entry.
    for cls_arg, value in cls_arg_value_pairs:
        assert getattr(entry, cls_arg) is value
