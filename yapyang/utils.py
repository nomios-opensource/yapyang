"""This module contains utilities."""

import typing as t

from yapyang.constants import DEFAULTS, XML_ATTRIBUTE_TEMPLATE


class MetaInfo:
    """YANG data model metadata information."""

    def __init__(
        self,
        default: t.Optional[t.Any] = None,
        attrs: t.Optional[dict[str, str]] = None,
    ) -> None:
        self.default = default
        self.attrs = attrs


def concatenate_xml_element_attrs(attrs: t.Optional[dict[str, str]]) -> str:
    """Concatenates XML element attributes."""

    element_attrs: str = ""
    if attrs:
        for attr, value in attrs.items():
            element_attrs += XML_ATTRIBUTE_TEMPLATE.format(attr, value)

    return element_attrs


def retrieve_xml_element_attrs(
    cls_meta: dict[str, t.Any], cls_arg: str, /
) -> t.Optional[dict]:
    """Retrieves XML element attributes from class meta for class arg."""

    if cls_attr_default := cls_meta[DEFAULTS].get(cls_arg):
        if isinstance(cls_attr_default, MetaInfo):
            return cls_attr_default.attrs

    return None
