"""This module contains utilities."""

import typing as t

XML_ATTRIBUTE_TEMPLATE: str = ' {0}="{1}"'


def concatenate_xml_element_attrs(attrs: t.Union[dict[str, str], None]) -> str:
    """Concatenates XML element attributes."""

    element_attrs: str = ""
    if attrs:
        for attr, value in attrs.items():
            element_attrs += XML_ATTRIBUTE_TEMPLATE.format(attr, value)

    return element_attrs
