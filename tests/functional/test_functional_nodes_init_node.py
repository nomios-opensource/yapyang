"""This module contains functional tests for nodes InitNode"""

import random
import string

import pytest

from yapyang.nodes import InitNode
from yapyang.utils import MetaInfo

ARGS: str = "__args__"
DEFAULTS: str = "__defaults__"


class Interfaces(InitNode):
    """Represents a subclass of InitNode."""

    name: str


def test_given_subclass_of_init_node_when_instantiated_with_args_then_args_are_assigned_in_order_of_annotated_cls_args():
    """Test given subclass of init node when instantiated with args then args are assigned in order of annotated cls args."""

    # Given subclass of InitNode annotated cls args.
    cls_args = Interfaces.__meta__[ARGS]

    # Given args.
    args = [random.choice(string.ascii_letters) for _ in cls_args]

    # When instantiated with args.
    interfaces = Interfaces(*args)

    # Then args are assigned in order of annotated cls args.
    for index, cls_arg in enumerate(cls_args):
        assert getattr(interfaces, cls_arg) is args[index]


def test_given_subclass_of_init_node_when_instantiated_with_kwargs_then_kwargs_are_assigned_for_annotated_cls_args():
    """Test given subclass of init node when instantiated with kwargs then kwargs are assigned for annotated cls args."""

    # Given subclass of InitNode annotated cls args.
    cls_args = Interfaces.__meta__[ARGS]

    # Given kwargs.
    kwargs = {
        cls_arg: random.choice(string.ascii_letters) for cls_arg in cls_args
    }

    # When instantiated with kwargs.
    interfaces = Interfaces(**kwargs)

    # Then kwargs are assigned for annotated cls args.
    for cls_arg in cls_args:
        assert getattr(interfaces, cls_arg) is kwargs[cls_arg]


def test_given_subclass_of_init_node_when_instantiated_without_args_or_kwargs_then_defaults_are_assigned_for_annotated_cls_args():
    """Test given subclass of init node when instantiated without args or kwargs then defaults are assigned for annotated cls args."""

    # Given subclass of InitNode annotated cls args.
    class InterfacesDefault(Interfaces):
        """Represents a subclass of InitNode."""

        name: str = "xe-0/0/0"

    cls_args = InterfacesDefault.__meta__[ARGS]

    # When instantiated without args or kwargs.
    interfaces = InterfacesDefault()

    # Then defaults are assigned for annotated cls args.
    for cls_arg in cls_args:
        assert (
            getattr(interfaces, cls_arg)
            is InterfacesDefault.__meta__[DEFAULTS][cls_arg]
        )


def test_given_subclass_of_init_node_with_meta_info_defaults_when_instantiated_without_args_or_kwargs_then_meta_info_default_are_assigned_for_annotated_cls_args():
    """Test given subclass of init node with meta info defaults when instantiated without args or kwargs then meta info default are assigned for annotated cls args."""

    # Given subclass of InitNode with MetaInfo default.
    meta_info = MetaInfo(default="xe-0/0/1")

    class Interfaces(InitNode):
        """Represents a subclass of InitNode"""

        name: str = meta_info

    # When instantiated without args or kwargs.
    interfaces = Interfaces()

    # Then MetaInfo.default are assigned for annotated cls args.
    assert interfaces.name is meta_info.default


def test_given_subclass_of_init_node_when_instantiated_with_too_many_args_or_kwargs_then_exception_is_raised():
    """Test given subclass of init node when instantiated with too many args or kwargs then exception is raised."""

    # Given subclass of InitNode subclass annotated cls args.
    cls_args = Interfaces.__meta__[ARGS]

    # Given too many args
    args = [random.choice(string.ascii_letters) for _ in cls_args]
    args.append("Too Many!")

    # When instantiated with args.
    with pytest.raises(TypeError) as exc:
        Interfaces(*args)

    # Then exception has expected message.
    assert (
        str(exc.value)
        == f"{Interfaces.__name__} takes {len(cls_args)} arguments, but {len(args)} were given."
    )


def test_given_subclass_of_init_node_when_instantiated_with_too_few_args_or_kwargs_then_exception_is_raised():
    """Test given subclass of init node when instantiated with too few args or kwargs then exception is raised."""

    # Given subclass of InitNode.

    # When instantiated with too few args.
    with pytest.raises(TypeError) as exc:
        Interfaces()

    # Then exception has expected message.
    assert str(exc.value) == "Missing required argument: name"
