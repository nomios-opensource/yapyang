"""This module contains unit tests for nodes Node."""

import random
import string
import types

import pytest

from yapyang.nodes import Node
from yapyang.utils import MetaInfo


class NodeSubclass(Node):
    """Represents a subclass of Node."""


class Person(NodeSubclass):
    """Represents a subclass of Node subclass."""

    __identifier__ = "person"

    firstname: str = "Jane"
    lastname: str = "Doe"


MOCK_NODE_CLS_ARGS = tuple(Person.__meta__["__args__"])  # type: ignore


def test_given_node_has_annotated_dunder_identifier_cls_attribute_when_node_object_created_then_node_meta_contains_cls_attribute_annotation():
    """Test given node has annotated dunder identifier cls attribute when node object created then node meta contains cls attribute annotation."""

    # Given Node has annotated dunder identifier cls attribute.
    __identifier__ = "__identifier__"

    # When Node object created.

    # Then Node meta contains cls attribute annotation.
    assert Node.__meta__[__identifier__] is str


def test_given_instance_of_subclass_of_node_subclass_when_resolve_cls_meta_args_is_called_with_args_then_yields_sequentially_cls_arg_and_arg_value_pair():
    """Test given instance of subclass of node subclass when resolve cls meta args is called with args then yields sequentially cls arg and arg value pair."""

    # Given args.
    args = tuple(
        random.choice(string.ascii_letters) for _ in MOCK_NODE_CLS_ARGS
    )

    # Given instance of subclass of Node subclass.
    instance = Person()

    # When resolve_cls_meta_args is called with args.
    generator = instance._resolve_cls_meta_args(args, dict())

    # Then generator is returned.
    assert isinstance(generator, types.GeneratorType)

    # Then yields sequentially cls_arg and arg value pair.
    for index, (cls_arg, value) in enumerate(generator):
        # Then in order cls args are defined.
        assert MOCK_NODE_CLS_ARGS[index] is cls_arg
        # Then in order args are given.
        assert args[index] is value


def test_given_instance_of_subclass_of_node_subclass_when_resolve_cls_meta_args_is_called_with_kwargs_then_yields_matched_cls_arg_and_kwarg_value_pair():
    """Test given instance of subclass of node subclass when resolve cls meta args is called with kwargs then yields matched cls arg and kwarg value pair."""

    # Given kwargs.
    kwargs = {
        cls_arg: random.choice(string.ascii_letters)
        for cls_arg in MOCK_NODE_CLS_ARGS
    }

    # Given instance of subclass of Node subclass.
    instance = Person()

    # When resolve_cls_meta_args is called with kwargs.
    generator = instance._resolve_cls_meta_args(tuple(), kwargs)

    # Then generator is returned.
    assert isinstance(generator, types.GeneratorType)

    # Then yields matched cls_arg and kwarg value pair.
    for cls_arg, value in generator:
        assert kwargs[cls_arg] is value


def test_given_instance_of_subclass_of_node_subclass_with_defaults_when_resolve_cls_meta_args_is_called_with_empty_args_and_kwargs_then_yields_matched_cls_arg_and_default_value_pair():
    """Test given instance of subclass of node subclass with defaults when resolve cls meta args is called with empty args and kwargs then yields matched cls arg and default value pair."""

    # Given instance of subclass of Node subclass.
    instance = Person()

    # When resolve_cls_meta_args is called with empty args and kwargs.
    generator = instance._resolve_cls_meta_args(tuple(), dict())

    # Then generator is returned.
    assert isinstance(generator, types.GeneratorType)

    # Then yields matched cls_arg and default value pair.
    for cls_arg, value in generator:
        assert Person.__meta__["__defaults__"][cls_arg] is value


def test_given_instance_of_subclass_of_node_subclass_with_meta_info_defaults_when_resolve_cls_meta_args_is_called_with_empty_args_and_kwargs_then_yields_matched_cls_args_and_default_meta_info_default_value_pair():
    """Test given instance of subclass of node subclass with meta info defaults when resolve cls meta args is called with empty args and kwargs then yields matched cls arg and default meta info default value pair."""

    # Given instance of subclass of Node subclass with MetaInfo defaults.
    class PersonMetaInfo(Person):
        firstname: str = MetaInfo(default="John")
        lastname: str = MetaInfo(default="Doe")

    instance = PersonMetaInfo()

    # When resolve_cls_meta_args is called with empty args and kwargs.
    generator = instance._resolve_cls_meta_args(tuple(), dict())

    # Then generator is returned.
    assert isinstance(generator, types.GeneratorType)

    # Then yields matched cls_arg and default MetaInfo.default value pair.
    for cls_arg, value in generator:
        assert (
            PersonMetaInfo.__meta__["__defaults__"][cls_arg].default is value
        )


def test_given_instance_of_subclass_of_node_subclass_when_resolve_cls_meta_args_is_called_with_too_many_args_or_kwargs_then_on_first_iteration_exception_is_raised():
    """Test given instance of subclass of node subclass when resolve cls meta args is called with too many args or kwargs then on first iteration exception is raised."""

    # Given instance of subclass of Node subclass.
    instance = Person()

    # Given format of exception message.
    exception_message = "{0} takes {1} arguments, but {2} were given."

    # When resolve_cls_meta_args is called with too many args.
    generator = instance._resolve_cls_meta_args(args := (1, 2, 3), dict())

    # Then on first iteration exception is raised.
    with pytest.raises(TypeError) as exc:
        generator.__next__()

    # Then exception has expected message.
    assert str(exc.value) == exception_message.format(
        Person.__name__, len(MOCK_NODE_CLS_ARGS), len(args)
    )

    # When resolve_cls_meta_args is called with too many kwargs.
    generator = instance._resolve_cls_meta_args(
        tuple(), kwargs := dict(one=1, two=2, three=3)
    )

    # Then on first iteration exception is raised.
    with pytest.raises(TypeError) as exc:
        generator.__next__()

    # Then exception has expected message.
    assert str(exc.value) == exception_message.format(
        Person.__name__, len(MOCK_NODE_CLS_ARGS), len(kwargs)
    )

    # When resolve_cls_meta_args is called with too many args and kwargs.
    generator = instance._resolve_cls_meta_args(
        args := (1, 2), kwargs := dict(three=3)
    )

    # Then on first iteration exception is raised.
    with pytest.raises(TypeError) as exc:
        generator.__next__()

    # Then exception has expected message.
    assert str(exc.value) == exception_message.format(
        Person.__name__, len(MOCK_NODE_CLS_ARGS), (len(args) + len(kwargs))
    )


def test_given_instance_of_subclass_of_node_subclass_when_resolve_cls_meta_args_is_called_with_too_few_args_or_kwargs_then_exception_is_raised():
    """Test given instance of subclass of node subclass when resolve cls meta args is called with too few args or kwargs then exception is raised."""

    # Given instance of subclass of Node subclass.
    class Person(NodeSubclass):
        """Represents a subclass of Node subclass."""

        __identifier__ = "person"

        firstname: str = "Jane"
        lastname: str

    instance = Person()

    # When resolve_cls_meta_args is called with too few args or kwargs.
    with pytest.raises(TypeError) as exc:
        tuple(instance._resolve_cls_meta_args(tuple(), dict()))

    # Then exception has expected message.
    assert str(exc.value) == "Missing required argument: lastname"
