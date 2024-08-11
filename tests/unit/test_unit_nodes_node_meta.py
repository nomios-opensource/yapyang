"""This module contains unit tests for nodes NodeMeta."""

from unittest.mock import Mock

import pytest

from yapyang.nodes import NodeMeta
from yapyang.utils import MetaInfo

ANNOTATIONS: str = "__annotations__"
META: str = "__meta__"
ARGS: str = "__args__"
DEFAULTS: str = "__defaults__"


def test_given_empty_namespace_empty_bases_when_construct_meta_is_called_then_namespace_contains_meta_args_and_defaults():
    """Test given empty namespace empty bases when construct meta is called then namespace contains meta, args and defaults."""

    # Given empty namespace.
    namespace = {}

    # When construct meta is called.
    NodeMeta._construct_meta(namespace, ())

    # Then namespace contains meta, args and defaults keys.
    assert META in namespace
    assert ARGS in namespace[META]
    assert DEFAULTS in namespace[META]


def test_given_namespace_with_attribute_annotations_when_construct_meta_is_called_then_attribute_annotations_removed_from_namespace():
    """Test given namespace with attribute annotations when construct meta is called then attribute annotations removed from namespace."""

    # Given namespace that contains attribute annotations key.
    namespace = {ANNOTATIONS: {"identifier": str}}

    # When construct meta is called.
    NodeMeta._construct_meta(namespace, ())

    # Then attribute annotations key removed from namespace.
    assert ANNOTATIONS not in namespace


def test_given_namespace_with_attribute_annotations_when_construct_meta_is_called_then_attribute_annotations_are_moved_to_namespace_meta_args():
    """Test given namespace with attribute annotations when construct meta is called then attribute annotations are moved to namespace meta args."""

    # Given namespace that contains attribute annotation.
    annotations = {"identifier": str}
    namespace = {ANNOTATIONS: annotations}

    # When construct meta is called.
    NodeMeta._construct_meta(namespace, ())

    # Then attribute annotation is moved to namespace meta args.
    assert namespace[META][ARGS] == annotations


def test_given_namespace_with_dunder_attribute_annotations_when_construct_meta_is_called_then_dunder_attribute_annotations_are_moved_to_namespace_meta():
    """Test given namespace with dunder attribute annotations when construct meta is called then dunder attribute annotations are moved to namespace meta."""

    # Given namespace that contains dunder attribute annotation.
    annotations = {"__identifier__": str}
    namespace = {ANNOTATIONS: annotations}

    # When construct meta is called.
    NodeMeta._construct_meta(namespace, ())

    # Then dunder attribute annotation is moved to namespace meta.
    assert annotations.items() <= namespace[META].items()


def test_given_namespace_with_attribute_annotations_that_has_defaults_when_construct_meta_is_called_then_attributes_defaults_are_removed_from_namespace_and_moved_to_namespace_meta_defaults():
    """Test given namespace with attribute annotations that has defaults when construct meta is called then attributes defaults are removed from namespace and moved to namespace meta defaults."""

    # Given attribute and default.
    cls_attribute, cls_attribute_default = ("identifier", "junos")

    # Given namespace that contains attribute annotation.
    namespace = {
        ANNOTATIONS: {cls_attribute: str},
        cls_attribute: cls_attribute_default,
    }

    # When construct meta is called.
    NodeMeta._construct_meta(namespace, ())

    # Then attribute removed from namespace.
    assert cls_attribute not in namespace

    # Then attribute default moved to namespace meta defaults.
    assert namespace[META][DEFAULTS][cls_attribute] is cls_attribute_default


def test_given_namespace_with_no_attribute_annotations_that_has_defaults_when_construct_meta_is_called_then_defaults_in_namespace():
    """Test given namespace with no attribute annotations that has defaults when construct meta is called then defaults in namespace."""

    # Given attribute and default.
    cls_attribute, cls_attribute_default = ("identifier", "junos")

    # Given namespace that contains attribute.
    namespace = {cls_attribute: cls_attribute_default}

    # When construct meta is called.
    NodeMeta._construct_meta(namespace, ())

    # Then attribute in namespace.
    assert namespace[cls_attribute] is cls_attribute_default


def test_given_base_with_meta_when_construct_meta_is_called_then_base_meta_copied_to_namespace_meta():
    """Test given base with meta when construct meta is called then base meta copied to namespace meta."""

    # Given base with meta.
    base = Mock()
    base.__meta__ = {"__identifier__": str, ARGS: {}, DEFAULTS: {}}

    # Given empty namespace.
    namespace = dict()

    # When construct meta is called.
    NodeMeta._construct_meta(namespace, (base,))

    # Then base meta copied to namespace meta.
    assert namespace[META] == base.__meta__


def test_given_base_with_meta_args_when_construct_meta_is_called_then_base_meta_args_copied_to_namespace_meta_args():
    """Test given base with meta args when construct meta is called then base meta args copied to namespace meta args."""

    # Given base with meta args.
    base = Mock()
    base.__meta__ = {ARGS: {"identifier": str}, DEFAULTS: {}}

    # Given empty namespace.
    namespace = dict()

    # When construct meta is called.
    NodeMeta._construct_meta(namespace, (base,))

    # Then base meta args copied to namespace meta args.
    assert namespace[META][ARGS] == base.__meta__[ARGS]


def test_given_base_with_meta_defaults_when_construct_meta_is_called_then_base_meta_defaults_copied_to_namespace_meta_defaults():
    """Test given base with meta defaults when construct meta is called then base meta defaults copied to namespace meta defaults."""

    # Given base with meta defaults.
    base = Mock()
    base.__meta__ = {
        ARGS: {"identifier": str},
        DEFAULTS: {"identifier": "cisco"},
    }

    # Given empty namespace.
    namespace = dict()

    # When construct meta is called.
    NodeMeta._construct_meta(namespace, (base,))

    # Then base meta defaults copied to namespace meta defaults.
    assert namespace[META][DEFAULTS] == base.__meta__[DEFAULTS]


def test_given_namespace_with_attribute_annotations_that_conflict_with_base_when_construct_meta_is_called_then_namespace_attribute_annotations_override_base():
    """Test given namespace with attribute annotations that conflict with base when construct meta is called then namespace attribute annotations override base."""

    # Given namespace that contains attribute annotation.
    annotations = {"identifier": str}
    namespace = {ANNOTATIONS: annotations}

    # Given base that contains conflicting attribute annotation.
    base = Mock()
    base.__meta__ = {ARGS: {"identifier": int}, DEFAULTS: {}}

    # When construct meta is called.
    NodeMeta._construct_meta(namespace, (base,))

    # Then namespace attribute annotation overrides base attribute annotation.
    assert namespace[META][ARGS] == annotations


def test_given_namespace_with_dunder_attribute_annotations_that_conflicts_with_base_when_construct_meta_is_called_then_namespace_dunder_attribute_annotations_override_base():
    """Test given namespace with dunder attribute annotations that conflicts with base when construct meta is called then namespace dunder attribute annotations override base."""

    # Given namespace that contains dunder attribute annotation.
    annotations = {"__identifier__": str}
    namespace = {ANNOTATIONS: annotations}

    # Given base that contains conflicting dunder attribute annotation.
    base = Mock()
    base.__meta__ = {"__identifier__": int, ARGS: {}, DEFAULTS: {}}

    # When construct meta is called.
    NodeMeta._construct_meta(namespace, (base,))

    # Then namespace dunder attribute annotation overrides base dunder attribute annotation.
    assert annotations.items() <= namespace[META].items()


def test_given_namespace_with_attribute_annotations_that_has_defaults_that_conflicts_with_base_when_construct_meta_is_called_then_namespace_defaults_override_base():
    """Test given namespace with attribute annotations that has defaults that conflicts with base when construct meta is called then namespace defaults override base."""

    # Given namespace that contains attribute annotation and default.
    cls_attribute, cls_attribute_default = ("identifier", "junos")
    namespace = {
        ANNOTATIONS: {cls_attribute: str},
        cls_attribute: cls_attribute_default,
    }

    # Given base that contains attribute annotation and conflicting default.
    base = Mock()
    base.__meta__ = {
        ARGS: {cls_attribute: str},
        DEFAULTS: {cls_attribute: "cisco"},
    }

    # When construct meta is called.
    NodeMeta._construct_meta(namespace, (base,))

    # Then namespace attribute annotation default overrides base.
    assert namespace[META][DEFAULTS][cls_attribute] is cls_attribute_default


def test_given_namespace_meta_with_attribute_defaults_not_of_annotation_when_meta_default_checker_is_called_then_exception_is_raised():
    """Test given namespace meta with attribute defaults not of annotation when meta default checker is called then exception is raised."""

    # Given namespace meta with attribute default not of annotation.
    namespace_meta = {
        (cls_attribute := "__identifier__"): (cls_attribute_annotation := str),
        ARGS: {},
        DEFAULTS: {cls_attribute: (cls_attribute_default := 1)},
    }

    # When meta default checker is called.
    with pytest.raises(TypeError) as exc:
        NodeMeta._meta_default_checker(namespace_meta)

    # Then exception has expected message.
    assert (
        str(exc.value)
        == f"Expected default of type {cls_attribute_annotation} for {cls_attribute}, got type {type(cls_attribute_default)}."
    )


def test_given_namespace_meta_with_attribute_defaults_of_annotation_when_meta_default_checker_is_called_then_exception_is_not_raised():
    """Test given namespace meta with attribute defaults of annotation when meta default checker is called then exception is not raised."""

    # Given namespace meta with attribute default of annotation.
    namespace_meta = {
        (cls_attribute := "__identifier__"): str,
        ARGS: {},
        DEFAULTS: {cls_attribute: "junos"},
    }

    # When meta default checker is called.
    NodeMeta._meta_default_checker(namespace_meta)

    # Then exception is not raised.


def test_given_namespace_meta_with_attribute_defaults_of_meta_info_when_meta_default_checker_is_called_then_exception_is_raised():
    """Test given namespace meta with attribute defaults of meta info when meta default checker is called then exception is raised."""

    # Given namespace meta with attribute default of MetaInfo.
    namespace_meta = {
        (cls_attribute := "__identifier__"): str,
        ARGS: {},
        DEFAULTS: {cls_attribute: MetaInfo()},
    }

    # When meta default checker is called.
    with pytest.raises(TypeError) as exc:
        NodeMeta._meta_default_checker(namespace_meta)

    # Then exception has expected message.
    assert (
        str(exc.value)
        == f"MetaInfo cannot be used on metadata attributes: {cls_attribute}"
    )


def test_given_namespace_meta_args_with_attribute_defaults_not_of_annotation_when_meta_default_checker_is_called_then_exception_is_raised():
    """Test given namespace meta args with attribute defaults not of annotation when meta default checker is called then exception is raised."""

    # Given namespace meta args with attribute default not of annotation.
    namespace_meta = {
        ARGS: {
            (cls_attribute := "identifier"): (cls_attribute_annotation := int),
        },
        DEFAULTS: {cls_attribute: (cls_attribute_default := "one")},
    }

    # When meta default checker is called.
    with pytest.raises(TypeError) as exc:
        NodeMeta._meta_default_checker(namespace_meta)

    # Then exception has expected message.
    assert (
        str(exc.value)
        == f"Expected default of type {cls_attribute_annotation} for {cls_attribute}, got type {type(cls_attribute_default)}."
    )


def test_given_namespace_meta_args_with_attribute_defaults_of_annotation_when_meta_default_checker_is_called_then_exception_is_not_raised():
    """Test given namespace meta args with attribute defaults of annotation when meta default checker is called then exception is not raised."""

    # Given namespace meta args with attribute default of annotation.
    namespace_meta = {
        ARGS: {
            (cls_attribute := "identifier"): int,
        },
        DEFAULTS: {cls_attribute: 1},
    }

    # When meta default checker is called.
    NodeMeta._meta_default_checker(namespace_meta)

    # Then exception is not raised.


def test_given_namespace_meta_args_with_attribute_defaults_of_meta_info_when_meta_default_checker_is_called_then_exception_is_not_raised():
    """Test given namespace meta args with attribute defaults of meta info when meta default checker is called then exception is not raised."""

    # Given namespace meta args with attribute default of MetaInfo.
    namespace_meta = {
        ARGS: {
            (cls_attribute := "identifier"): float,
        },
        DEFAULTS: {cls_attribute: MetaInfo()},
    }
    # When meta default checker is called.
    NodeMeta._meta_default_checker(namespace_meta)

    # Then exception is not raised.


def test_given_namespace_meta_args_with_attribute_defaults_of_meta_info_and_default_not_of_annotation_when_meta_default_checker_is_called_then_exception_is_raised():
    """Test given namespace meta args with attribute defaults of meta info and default not of annotation when meta default checker is called then exception is raised."""

    # Given namespace meta args with attribute default of MetaInfo,
    # and MetaInfo.default not of annotation.
    namespace_meta = {
        ARGS: {
            (cls_attribute := "identifier"): (cls_attribute_annotation := str),
        },
        DEFAULTS: {cls_attribute: MetaInfo((cls_attribute_default := 1))},
    }

    # When meta default checker is called.
    with pytest.raises(TypeError) as exc:
        NodeMeta._meta_default_checker(namespace_meta)

    # Then exception has expected message.
    assert (
        str(exc.value)
        == f"Expected default of type {cls_attribute_annotation} for {cls_attribute}, got type {type(cls_attribute_default)}."
    )
