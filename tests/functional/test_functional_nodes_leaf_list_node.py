"""This module contains functional tests for nodes LeafListNode."""

from yapyang.nodes import LeafListNode


class User(LeafListNode):
    """Represents a subclass of LeafListNode."""

    __identifier__: str = "user"

    value: str


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

    # When to_xml is called with attrs.
    xml = user.to_xml(attrs={"operation": "create"})

    # Then for each entry XML element with attrs returned.
    assert (
        xml
        == f'<user operation="create">{john}</user><user operation="create">{jane}</user>'
    )
