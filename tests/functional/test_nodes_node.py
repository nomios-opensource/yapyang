"""This module contains tests for nodes Node."""

import pytest

from yapyang.nodes import ModuleNode, Node


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

    # When node subclass is instantiated.
    with pytest.raises(TypeError) as exc:
        ModuleNode()

    # Then exception has expected message.
    assert (
        str(exc.value)
        == "Node or subclasses of cannot be directly instantiated."
    )


def test_given_subclass_of_node_subclass_when_instantiated_then_exception_is_not_raised():
    """Test given subclass of node subclass when instantiated then exception is not raised."""

    # Given subclass of node subclass.
    class MockModule(ModuleNode):
        """Mock module node."""

    # When MockModule is instantiated.
    MockModule()

    # Then exception is not raised.
