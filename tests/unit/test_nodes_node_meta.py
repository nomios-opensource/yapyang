"""This module contains unit tests for nodes NodeMeta."""

from unittest.mock import Mock

from yapyang.nodes import NodeMeta

ANNOTATIONS: str = "__annotations__"
METADATA: str = "__metadata__"


def test_given_empty_namespace_empty_bases_when_construct_metadata_is_called_then_namespace_contains_metadata_and_annotations():
    """Test given empty namespace empty bases when construct metadata is called then namespace contains metadata and annotations."""

    # Given empty namespace.
    namespace = {}

    # When construct metadata is called.
    NodeMeta._construct_metadata(namespace, ())

    # Then namespace contains metadata and annotations keys.
    assert METADATA in namespace
    assert ANNOTATIONS in namespace[METADATA]


def test_given_namespace_with_annotations_when_construct_metadata_is_called_then_annotations_are_removed_from_namespace_and_copied_to_metadata_annotations():
    """Test given namespace with annotations when construct metadata is called then annotations are removed from namespace and copied to metadata annotations."""

    # Given namespace that contains annotations.
    annotations = {"identifier": str}
    namespace = {ANNOTATIONS: annotations}

    # When construct metadata is called.
    NodeMeta._construct_metadata(namespace, ())

    # Then annotations key removed from namespace.
    assert ANNOTATIONS not in namespace

    # Then annotations are copied to namespace metadata annotations.
    assert namespace[METADATA][ANNOTATIONS] == annotations


def test_given_namespace_with_annotations_that_has_defaults_when_construct_metadata_is_called_then_defaults_removed_from_namespace_and_moved_to_metadata():
    """Test given namespace with annotations that has defaults when construct metadata is called then defaults removed from namespace and moved to metadata."""

    # Given attribute and default.
    cls_attribute, cls_attribute_default = ("identifier", "junos")

    # Given namespace that contains attribute and has annotation.
    annotations = {cls_attribute: str}
    namespace = {
        ANNOTATIONS: annotations,
        cls_attribute: cls_attribute_default,
    }

    # When construct metadata is called.
    NodeMeta._construct_metadata(namespace, ())

    # Then attribute removed from namespace.
    assert cls_attribute not in namespace

    # Then attribute and default moved to namespace metadata.
    assert namespace[METADATA][cls_attribute] is cls_attribute_default


def test_given_namespace_with_no_annotations_that_has_defaults_when_construct_metadata_is_called_then_defaults_in_namespace():
    """Test given namespace with no annotations that has defaults when construct metadata is called then defaults in namespace."""

    # Given attribute and default.
    cls_attribute, cls_attribute_default = ("identifier", "junos")

    # Given namespace that contains attribute.
    namespace = {cls_attribute: cls_attribute_default}

    # When construct metadata is called.
    NodeMeta._construct_metadata(namespace, ())

    # Then attribute in namespace.
    assert cls_attribute in namespace
    assert namespace[cls_attribute] is cls_attribute_default


def test_given_base_with_metadata_annotations_when_construct_metadata_is_called_then_base_metadata_annotations_copied_to_namespace_metadata_annotations():
    """Test given base with metadata annotations when construct metadata is called then base metadata annotations copied to namespace metadata annotations."""

    # Given base with metadata annotations.
    base = Mock()
    base.__metadata__ = {ANNOTATIONS: {"identifier": str}}

    # Given empty namespace.
    namespace = dict()

    # When construct metadata is called.
    NodeMeta._construct_metadata(namespace, (base,))

    # Then base metadata annotations copied to namespace metadata annotations.
    assert namespace[METADATA][ANNOTATIONS] == base.__metadata__[ANNOTATIONS]


def test_given_base_with_metadata_annotations_that_has_defaults_when_construct_metadata_is_called_then_base_metadata_defaults_copied_to_namespace_metadata():
    """Test given base with metadata annotations that has defaults when construct metadata is called then base metadata defaults coped to namespace metadata."""

    # Given base with metadata defaults.
    base = Mock()
    base.__metadata__ = {
        ANNOTATIONS: {"identifier": str},
        "identifier": "junos",
    }

    # Given empty namespace.
    namespace = dict()

    # When construct metadata is called.
    NodeMeta._construct_metadata(namespace, (base,))

    # Then base metadata defaults copied to namespace metadata.
    assert namespace[METADATA] == base.__metadata__


def test_given_namespace_with_annotations_and_conflicts_in_base_when_construct_metadata_is_called_then_namespace_annotations_override_base():
    """Test given namespace with annotations and conflicts in base when construct metadata is called then namespace annotations override base."""

    # Given namespace that contains annotations.
    annotations = {"identifier": str}
    namespace = {ANNOTATIONS: annotations}

    # Given base that contains conflicting annotations.
    base = Mock()
    base.__metadata__ = {ANNOTATIONS: {"identifier": int}}

    # When construct metadata is called.
    NodeMeta._construct_metadata(namespace, (base,))

    # Then namespace annotations override base annotations.
    assert namespace[METADATA][ANNOTATIONS] == annotations


def test_given_namespace_with_annotations_that_has_defaults_and_conflicts_in_base_when_construct_metadata_is_called_then_namespace_defaults_override_base():
    """Test given namespace with annotations that has defaults and conflicts in base when construct metadata is called then namespace defaults override base."""

    # Given namespace that contains attribute and has annotation.
    cls_attribute, cls_attribute_default = ("identifier", "junos")
    annotations = {cls_attribute: str}
    namespace = {
        ANNOTATIONS: annotations,
        cls_attribute: cls_attribute_default,
    }

    # Given base that contains attribute.
    base = Mock()
    base.__metadata__ = {
        ANNOTATIONS: {cls_attribute: str},
        cls_attribute: "cisco",
    }

    # When construct metadata is called.
    NodeMeta._construct_metadata(namespace, (base,))

    # Then namespace attribute override base attribute.
    assert namespace[METADATA][cls_attribute] is cls_attribute_default


def test_given_args_when_node_meta_new_method_called_then_construct_metadata_is_called_once():
    """Test given args when node meta new method called then construct metadata is called once."""

    # Given mock construct metadata.
    NodeMeta._construct_metadata = Mock()

    # When new is called.
    NodeMeta.__new__(NodeMeta, "MockClass", (), {})

    # Then construct metadata is called once.
    NodeMeta._construct_metadata.assert_called_once()
