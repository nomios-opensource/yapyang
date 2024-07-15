"""This module contains functional tests for ModuleNode."""

import random
import pytest
import string

from yapyang.nodes import ModuleNode


class MockModule(ModuleNode):
    """Represents a subclass of ModuleNode."""


def test_given_subclass_of_module_node_when_instantiated_with_args_then_args_are_assigned_in_order_of_annotated_cls_attributes():
    """Test given subclass of module node when instantiated with args then args are assigned in order of annotated cls attributes."""

    # Given MockModule annotated cls attributes.
    cls_attributes = MockModule.__metadata__["__annotations__"]

    # Given args.
    args = [
        random.choice(string.ascii_letters) for attribute in cls_attributes
    ]

    # When MockModule is instantiated with args.
    module = MockModule(*args)

    # Then args are assigned in order of annotated cls attributes.
    for index, cls_attribute in enumerate(cls_attributes):
        assert getattr(module, cls_attribute) is args[index]


def test_given_subclass_of_module_node_when_instantiated_with_kwargs_then_kwargs_are_assigned_for_annotated_cls_attributes():
    """Test given subclass of module node when instantiated with kwargs then kwargs are assigned for annotated cls attributes."""

    # Given MockModule annotated cls attributes.
    cls_attributes = MockModule.__metadata__["__annotations__"]

    # Given kwargs.
    kwargs = {
        attr: random.choice(string.ascii_letters) for attr in cls_attributes
    }

    # When MockModule is instantiated with kwargs.
    module = MockModule(**kwargs)

    # Then kwargs are assigned for annotated cls attributes.
    for cls_attribute in cls_attributes:
        assert getattr(module, cls_attribute) is kwargs[cls_attribute]


def test_given_subclass_of_module_node_when_instantiated_without_args_or_kwargs_then_defaults_are_assigned_for_annotated_cls_attributes():
    """Test given subclass of module node when instantiated without args or kwargs then defaults are assigned for annotated cls attributes."""

    # Given MockModule annotated cls attributes.
    cls_attributes = MockModule.__metadata__["__annotations__"]

    # When MockModule is instantiated without args or kwargs.
    module = MockModule()

    # Then defaults are assigned for annotated cls attributes.
    for cls_attribute in cls_attributes:
        assert (
            getattr(module, cls_attribute)
            is MockModule.__metadata__[cls_attribute]
        )


def test_given_subclass_of_module_node_when_instantiated_with_too_many_args_or_kwargs_then_exception_is_raised():
    """Test given subclass of module node when instantiated with too many args or kwargs then exception is raised."""

    # Given MockModule annotated cls attributes.
    cls_attributes = MockModule.__metadata__["__annotations__"]

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


def test_given_subclass_of_module_node_when_instantiated_with_too_few_args_or_kwargs_then_exception_is_raised():
    """Test given subclass of module node when instantiated with too few args or kwargs then exception is raised."""

    # Given RevisionMockModule.
    class RevisionMockModule(MockModule):
        revision: str

    # Given too few args (for MockModule)
    args = [
        random.choice(string.ascii_letters)
        for attribute in MockModule.__metadata__["__annotations__"]
    ]

    # When RevisionMockModule is instantiated with args.
    with pytest.raises(TypeError) as exc:
        RevisionMockModule(*args)

    # Then exception has expected message.
    assert str(exc.value) == "Missing required argument: revision "
