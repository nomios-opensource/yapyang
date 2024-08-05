"""This module contains functional tests for nodes LeafListNode."""

import pytest
from ordered_set import OrderedSet

from yapyang.nodes import LeafListNode


class User(LeafListNode):
    """Represents a subclass of LeafListNode."""

    __identifier__: str = "user"

    value: str


def test_given_subclass_of_leaf_list_node_when_instantiated_then_entries_attribute_created():
    """Test given subclass of leaf list node when instantiated then entries attribute created."""

    # Given subclass of LeafListNode.

    # When instantiated.
    user = User()

    # Then entries attribute created.
    assert "entries" in user.__dict__
    assert isinstance(user.entries, OrderedSet)


def test_given_instance_of_leaf_list_node_subclass_when_append_is_called_with_value_then_value_entry_contained_in_entries():
    """Test given instance of leaf list node subclass when append is called with value then value entry contained in entries"""

    # Given instance of LeafListNode subclass.
    user = User()

    # When append is called with value.
    user.append((value := "Jane Doe"))

    # Then value entry contained in entries.
    assert value in user.entries


def test_given_instance_of_leaf_list_node_subclass_when_append_is_called_without_value_then_default_entry_contained_in_entries():
    """Test given instance of leaf list node subclass when append is called without value then default entry contained in entries"""

    # Given instance of LeafListNode subclass with default value.
    default = "John Doe"

    class UserDefault(User):
        value: str = default

    user = UserDefault()

    # When append is called without value.
    user.append()

    # Then default entry contained in entries.
    assert default in user.entries


def test_given_instance_of_leaf_list_node_subclass_when_append_is_called_with_too_many_values_then_exception_is_raised():
    """Test given instance of leaf list node subclass when append is called with too many values then exception is raised."""

    # Given instance of LeafListNode subclass.
    user = User()

    # When append is called with too many values.
    with pytest.raises(TypeError) as exc:
        user.append("John Doe", "Jane Doe")

    # Then exception has expected message.
    assert (
        str(exc.value)
        == f"{User.__name__} takes 1 arguments, but 2 were given."
    )


def test_given_instance_of_leaf_list_node_subclass_when_append_is_called_with_too_few_values_then_exception_is_raised():
    """Test given instance of leaf list node subclass when append is called with too few values then exception is raised."""

    # Given instance of LeafListNode subclass.
    user = User()

    # When append is called with too few values.
    with pytest.raises(TypeError) as exc:
        user.append()

    # Then exception has expected message.
    assert str(exc.value) == "Missing required argument: value"


def test_given_instance_of_leaf_list_node_subclass_with_entries_when_to_xml_is_called_then_for_each_entry_xml_element_returned():
    """Test given instance of leaf list node subclass with entries when to xml is called then for each entry xml element returned."""

    # Given instance of LeafListNode subclass with entries.
    user = User()
    user.append((john := "John Doe"))
    user.append((jane := "Jane Doe"))

    # When to_xml is called.
    xml = user.to_xml()

    # Then for each entry XML element returned.
    assert xml == f"<user>{john}</user><user>{jane}</user>"


def test_given_instance_of_leaf_list_node_subclass_with_entries_when_to_xml_is_called_with_attrs_then_for_each_entry_xml_element_with_attrs_returned():
    """Test given instance of leaf list node subclass with entries when to xml is called with attrs then for each entry xml element with attrs returned."""

    # Given instance of LeafListNode subclass with entries.
    user = User()
    user.append((john := "John Doe"))
    user.append((jane := "Jane Doe"))

    # When to_xml is called.
    xml = user.to_xml(attrs={"operation": "create"})

    # Then for each entry XML element with attrs returned.
    assert (
        xml
        == f'<user operation="create">{john}</user><user operation="create">{jane}</user>'
    )
