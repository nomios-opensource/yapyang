"""This module contains unit tests for nodes Node."""

import typing as t

from yapyang.nodes import Node


def test_given_node_has_annotated_dunder_identifier_cls_attribute_when_node_object_created_then_node_meta_contains_cls_attribute_annotation_and_default():
    """Test given node has annotated dunder identifier cls attribute when node object created then node meta contains cls attribute annotation and default."""

    # Given Node has annotated dunder identifier cls attribute.
    __identifier__ = "__identifier__"

    # When Node object created.

    # Then Node meta contains cls attribute annotation.
    assert Node.__meta__[__identifier__] is t.Optional[str]

    # Then Node meta defaults contains cls attribute default.
    assert Node.__meta__["__defaults__"][__identifier__] is None
