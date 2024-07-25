"""This module contains functional tests for nodes Node."""

import random
import pytest
import string

from yapyang.nodes import Node
from yapyang.utils import MetaInfo

ARGS: str = "__args__"
DEFAULTS: str = "__defaults__"


class ContainerNode(Node):
    """Represents a subclass of Node."""


class Interfaces(ContainerNode):
    """Represents a subclass of ContainerNode."""

    name: str = "xe-0/0/0"


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
        ContainerNode()

    # Then exception has expected message.
    assert (
        str(exc.value)
        == "Node or subclasses of cannot be directly instantiated."
    )


def test_given_subclass_of_node_subclass_when_instantiated_then_exception_is_not_raised():
    """Test given subclass of node subclass when instantiated then exception is not raised."""

    # Given subclass of Node subclass.

    # When instantiated.
    Interfaces()

    # Then exception is not raised.


def test_given_subclass_of_node_subclass_when_instantiated_with_args_then_args_are_assigned_in_order_of_annotated_cls_attributes():
    """Test given subclass of node subclass when instantiated with args then args are assigned in order of annotated cls attributes."""

    # Given subclass of Node subclass annotated cls attributes.
    cls_attributes = Interfaces.__meta__[ARGS]

    # Given args.
    args = [random.choice(string.ascii_letters) for _ in cls_attributes]

    # When instantiated with args.
    instance = Interfaces(*args)

    # Then args are assigned in order of annotated cls attributes.
    for index, cls_attribute in enumerate(cls_attributes):
        assert getattr(instance, cls_attribute) is args[index]


def test_given_subclass_of_node_subclass_when_instantiated_with_kwargs_then_kwargs_are_assigned_for_annotated_cls_attributes():
    """Test given subclass of node subclass when instantiated with kwargs then kwargs are assigned for annotated cls attributes."""

    # Given subclass of Node subclass annotated cls attributes.
    cls_attributes = Interfaces.__meta__[ARGS]

    # Given kwargs.
    kwargs = {
        attr: random.choice(string.ascii_letters) for attr in cls_attributes
    }

    # When instantiated with kwargs.
    instance = Interfaces(**kwargs)

    # Then kwargs are assigned for annotated cls attributes.
    for cls_attribute in cls_attributes:
        assert getattr(instance, cls_attribute) is kwargs[cls_attribute]


def test_given_subclass_of_node_subclass_when_instantiated_without_args_or_kwargs_then_defaults_are_assigned_for_annotated_cls_attributes():
    """Test given subclass of node subclass when instantiated without args or kwargs then defaults are assigned for annotated cls attributes."""

    # Given subclass of Node subclass annotated cls attributes.
    cls_attributes = Interfaces.__meta__[ARGS]

    # When instantiated without args or kwargs.
    instance = Interfaces()

    # Then defaults are assigned for annotated cls attributes.
    for cls_attribute in cls_attributes:
        assert (
            getattr(instance, cls_attribute)
            is Interfaces.__meta__[DEFAULTS][cls_attribute]
        )


def test_given_subclass_of_node_subclass_with_meta_info_defaults_when_instantiated_without_args_or_kwargs_then_meta_info_default_are_assigned_for_annotated_cls_attributes():
    """Test given subclass of node subclass with meta info defaults when instantiated without args or kwargs then meta info default are assigned for annotated cls attributes."""

    # Given subclass of Node subclass with MetaInfo default.
    meta_info = MetaInfo(default="xe-0/0/1")

    class Interfaces(ContainerNode):
        """Represents a subclass of ContainerNode"""

        name: str = meta_info

    # When instantiated without args or kwargs.
    instance = Interfaces()

    # Then MetaInfo.default are assigned for annotated cls attributes.
    assert instance.name is meta_info.default


def test_given_subclass_of_node_subclass_when_instantiated_with_too_many_args_or_kwargs_then_exception_is_raised():
    """Test given subclass of node subclass when instantiated with too many args or kwargs then exception is raised."""

    # Given subclass of Node subclass annotated cls attributes.
    cls_attributes = Interfaces.__meta__[ARGS]

    # Given too many args
    args = [
        random.choice(string.ascii_letters) for attribute in cls_attributes
    ]
    args.append("Too Many!")

    # When instantiated with args.
    with pytest.raises(TypeError) as exc:
        Interfaces(*args)

    # Then exception has expected message.
    assert (
        str(exc.value)
        == f"{Interfaces.__name__} takes {len(cls_attributes)} arguments, but {len(args)} were given."
    )


def test_given_subclass_of_node_subclass_when_instantiated_with_too_few_args_or_kwargs_then_exception_is_raised():
    """Test given subclass of node subclass when instantiated with too few args or kwargs then exception is raised."""

    # Given subclass of node subclass.
    class NewInterfaces(Interfaces):
        ether_options: str

    # Given too few args.
    args = [
        random.choice(string.ascii_letters) for _ in Interfaces.__meta__[ARGS]
    ]

    # When instantiated with args.
    with pytest.raises(TypeError) as exc:
        NewInterfaces(*args)

    # Then exception has expected message.
    assert str(exc.value) == "Missing required argument: ether_options"
