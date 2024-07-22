"""This module contains functional tests for nodes Node."""

import random
import pytest
import string

from yapyang.nodes import Node

ARGS: str = "__args__"
DEFAULTS: str = "__defaults__"


class ModuleNode(Node):
    """Represents a subclass of Node."""


class MockModule(ModuleNode):
    """Represents a subclass of ModuleNode."""

    namespace: str = "cisco"


def test_when_node_instantiated_then_exception_is_raised():
    """Test when node instantiated then exception is raised."""

    # When Node is instantiated.
    with pytest.raises(TypeError) as exc:
        Node()

    # Then exception has expected message.
    assert (
        str(exc.value)
        == "Node or subclasses of cannot be directly instantiated."
    )


def test_when_node_subclass_instantiated_then_exception_is_raised():
    """Test when node subclass instantiated then exception is raised."""

    # When Node subclass is instantiated.
    with pytest.raises(TypeError) as exc:
        ModuleNode()

    # Then exception has expected message.
    assert (
        str(exc.value)
        == "Node or subclasses of cannot be directly instantiated."
    )


def test_given_subclass_of_node_subclass_when_instantiated_then_exception_is_not_raised():
    """Test given subclass of node subclass when instantiated then exception is not raised."""

    # Given MockModule subclass of Node subclass.

    # When MockModule is instantiated.
    MockModule()

    # Then exception is not raised.


def test_given_subclass_of_node_subclass_when_instantiated_with_args_then_args_are_assigned_in_order_of_annotated_cls_attributes():
    """Test given subclass of node subclass when instantiated with args then args are assigned in order of annotated cls attributes."""

    # Given MockModule annotated cls attributes.
    cls_attributes = MockModule.__meta__[ARGS]

    # Given args.
    args = [random.choice(string.ascii_letters) for _ in cls_attributes]

    # When MockModule is instantiated with args.
    module = MockModule(*args)

    # Then args are assigned in order of annotated cls attributes.
    for index, cls_attribute in enumerate(cls_attributes):
        assert getattr(module, cls_attribute) is args[index]


def test_given_subclass_of_node_subclass_when_instantiated_with_kwargs_then_kwargs_are_assigned_for_annotated_cls_attributes():
    """Test given subclass of node subclass when instantiated with kwargs then kwargs are assigned for annotated cls attributes."""

    # Given MockModule annotated cls attributes.
    cls_attributes = MockModule.__meta__[ARGS]

    # Given kwargs.
    kwargs = {
        attr: random.choice(string.ascii_letters) for attr in cls_attributes
    }

    # When MockModule is instantiated with kwargs.
    module = MockModule(**kwargs)

    # Then kwargs are assigned for annotated cls attributes.
    for cls_attribute in cls_attributes:
        assert getattr(module, cls_attribute) is kwargs[cls_attribute]


def test_given_subclass_of_node_subclass_when_instantiated_without_args_or_kwargs_then_defaults_are_assigned_for_annotated_cls_attributes():
    """Test given subclass of node subclass when instantiated without args or kwargs then defaults are assigned for annotated cls attributes."""

    # Given MockModule annotated cls attributes.
    cls_attributes = MockModule.__meta__[ARGS]

    # When MockModule is instantiated without args or kwargs.
    module = MockModule()

    # Then defaults are assigned for annotated cls attributes.
    for cls_attribute in cls_attributes:
        assert (
            getattr(module, cls_attribute)
            is MockModule.__meta__[DEFAULTS][cls_attribute]
        )


def test_given_subclass_of_node_subclass_when_instantiated_with_too_many_args_or_kwargs_then_exception_is_raised():
    """Test given subclass of node subclass when instantiated with too many args or kwargs then exception is raised."""

    # Given MockModule annotated cls attributes.
    cls_attributes = MockModule.__meta__[ARGS]

    # Given too many args
    args = [
        random.choice(string.ascii_letters) for attribute in cls_attributes
    ]
    args.append("Too Many!")

    # When MockModule is instantiated with args.
    with pytest.raises(TypeError) as exc:
        MockModule(*args)

    # Then exception has expected message.
    assert (
        str(exc.value)
        == f"{MockModule.__name__} takes {len(cls_attributes)} arguments, but {len(args)} were given."
    )


def test_given_subclass_of_node_subclass_when_instantiated_with_too_few_args_or_kwargs_then_exception_is_raised():
    """Test given subclass of node subclass when instantiated with too few args or kwargs then exception is raised."""

    # Given RevisionMockModule.
    class RevisionMockModule(MockModule):
        revision: str  # type: ignore

    # Given too few args (for MockModule)
    args = [
        random.choice(string.ascii_letters)
        for attribute in MockModule.__meta__[ARGS]
    ]

    # When RevisionMockModule is instantiated with args.
    with pytest.raises(TypeError) as exc:
        RevisionMockModule(*args)

    # Then exception has expected message.
    assert str(exc.value) == "Missing required argument: revision"
