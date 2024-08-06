"""This module contains functional tests for nodes Node."""

import pytest

from yapyang.nodes import Node


class ContainerNode(Node):
    """Represents a subclass of Node."""


class Interfaces(ContainerNode):
    """Represents a subclass of ContainerNode."""


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
