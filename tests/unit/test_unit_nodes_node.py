"""This module contains unit tests for nodes Node."""

import typing as t

from yapyang.nodes import Node


def test_given_node_has_annotated_identifier_attribute_when_node_object_created_then_node_metadata_contains_attribute_annotation_and_default():
    """Test given node has annotated identifier attribute when node object created then node metadata contains attribute annotation and default."""

    # Given Node has annotated identifier attribute.
    identifier = "identifier"

    # When Node object created.

    # Then Node metadata contains identifier attribute annotation.
    assert Node.__metadata__["__annotations__"][identifier] is t.Optional[str]

    # Then Node metadata contains identifier attribute default.
    assert Node.__metadata__[identifier] is None
