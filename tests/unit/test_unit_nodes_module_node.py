"""This module contains unit tests for nodes ModuleNode."""

import typing as t

from yapyang.nodes import ModuleNode


def test_given_module_node_has_annotated_dunder_namespace_cls_attribute_when_module_node_object_created_then_module_node_meta_contains_cls_attribute_annotation_and_default():
    """Test given module node has annotated dunder namespace cls attribute when module node object created then module node meta contains cls attribute annotation and default."""

    # Given ModuleNode has annotated dunder namespace cls attribute.
    __namespace__ = "__namespace__"

    # When ModuleNode object created.

    # Then ModuleNode meta contains cls attribute annotation.
    assert ModuleNode.__meta__[__namespace__] is t.Optional[str]

    # Then ModuleNode meta defaults contains cls attribute default.
    assert ModuleNode.__meta__["__defaults__"][__namespace__] is None
