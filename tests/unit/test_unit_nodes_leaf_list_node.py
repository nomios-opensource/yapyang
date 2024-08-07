"""This module contains unit tests for nodes LeafListNode."""

from unittest.mock import MagicMock, patch

from ordered_set import OrderedSet

from yapyang.nodes import LeafListNode, Node


class MockLeafListNode(LeafListNode):
    """Represents a subclass of LeafListNode."""


def test_given_leaf_list_node_subclass_when_instantiated_then_entries_attribute_created():
    """Test given leaf list node subclass when instantiated then entries attribute created."""

    # Given LeafListNode subclass.

    # When instantiated.
    user = MockLeafListNode()

    # Then entries attribute created.
    assert "entries" in user.__dict__
    assert isinstance(user.entries, OrderedSet)


@patch.object(Node, "__init__")
def test_given_leaf_list_node_subclass_when_instantiated_then_node_initializer_called(
    node_init,
):
    """Test given leaf list node subclass when instantiated then node initializer called."""

    # Given LeafListNode subclass.

    # When instantiated.
    MockLeafListNode()

    # Then Node __init__ Mock was called.
    node_init.assert_called()


def test_given_instance_of_leaf_list_node_subclass_when_append_is_called_with_value_then_cls_meta_args_resolver_yielded_value_is_added_to_entries():
    """Test given instance of leaf list node subclass when append is called with value then cls meta args resolver yielded value is added to entries."""

    # Given value.
    value = ("mock_value",)

    # Given tuple of cls_arg, value pairs.
    cls_arg_value_pairs = (("firstname", "John"), ("lastname", "Doe"))

    # Given Mock iterator with __iter__ method that returns a tuple
    # containing cls_arg, value pairs.
    mock_iterator = MagicMock()
    mock_iterator.__iter__.return_value = cls_arg_value_pairs

    # Given Mock _cls_meta_args_resolver that returns Mock iterator
    # when called.
    mock = MagicMock(return_value=mock_iterator)
    MockLeafListNode._cls_meta_args_resolver = mock

    # Given instance of LeafListNode subclass.
    instance = MockLeafListNode()

    # When append is called with value.
    instance.append(*value)

    # Then Mock _cls_meta_args_resolver was called with value.
    MockLeafListNode._cls_meta_args_resolver.assert_called_once_with(
        value, dict()
    )

    # Then Mock iterator __iter__ was called.
    mock_iterator.__iter__.assert_called()

    # Then cls_arg, value pairs value are added to entries.
    for _, value in cls_arg_value_pairs:
        assert value in instance.entries
