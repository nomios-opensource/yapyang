"""This module contains unit tests for nodes ModuleNode."""

import typing as t

from yapyang.nodes import ModuleNode


def test_given_module_node_has_annotated_namespace_attribute_when_module_node_object_created_then_module_node_metadata_contains_attribute_annotation_and_default():
    """Test given module node has annotated namespace attribute when module node object created then module node metadata contains attribute annotation and default."""

    # Given ModuleNode has annotated namespace attribute.
    namespace = "namespace"

    # When ModuleNode object created.

    # Then ModuleNode metadata contains namespace attribute annotation.
    assert (
        ModuleNode.__metadata__["__annotations__"][namespace]
        is t.Optional[str]
    )

    # Then ModuleNode metadata contains namespace attribute default.
    assert ModuleNode.__metadata__[namespace] is None
