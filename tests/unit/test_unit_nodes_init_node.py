"""This module contains unit tests for nodes InitNode."""

from unittest.mock import MagicMock, patch

import pytest

from yapyang.nodes import InitNode, Node


class InitNodeSubclass(InitNode):
    """Represents a subclass of InitNode."""

    __identifier__ = "init_node_subclass"


@patch.object(Node, "__init__")
def test_given_init_node_subclass_when_instantiated_then_node_initializer_called(
    node_init,
):
    """Test given init node subclass when instantiated then node initializer called."""

    # Given InitNode subclass.

    # When instantiated.
    with pytest.raises(AttributeError):
        # Then exception is raised for attributes that Node __init__
        # Mock did not create.
        InitNodeSubclass()

    # Then Node __init__ Mock was called.
    node_init.assert_called()


def test_given_init_node_subclass_when_instantiated_with_args_and_kwargs_then_resolve_cls_meta_args_yielded_cls_arg_value_pairs_are_set_as_attributes():
    """Test given init node subclass when instantiated with args and kwargs then resolve cls meta args yielded cls arg value pairs are set as attributes."""

    # Given args and kwargs.
    args = (1, 2, 3, 4, 5)
    kwargs = {"one": 1, "two": 2}

    # Given tuple of cls_arg, value pairs.
    cls_arg_value_pairs = (("firstname", "John"), ("lastname", "Doe"))

    # Given Mock iterator with __iter__ method that returns a tuple
    # containing cls_arg, value pairs.
    mock_iterator = MagicMock()
    mock_iterator.__iter__.return_value = cls_arg_value_pairs

    # Given Mock _resolve_cls_meta_args that returns Mock iterator
    # when called.
    mock = MagicMock(return_value=mock_iterator)
    InitNodeSubclass._resolve_cls_meta_args = mock

    # When instantiated with args and kwargs.
    instance = InitNodeSubclass(*args, **kwargs)

    # Then Mock _resolve_cls_meta_args was called with args and kwargs.
    InitNodeSubclass._resolve_cls_meta_args.assert_called_once_with(
        args, kwargs
    )

    # Then Mock iterator __iter__ was called.
    mock_iterator.__iter__.assert_called()

    # Then cls_arg, value pairs are set as attributes.
    for cls_arg, value in cls_arg_value_pairs:
        assert getattr(instance, cls_arg) is value
