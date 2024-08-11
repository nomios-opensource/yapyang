"""
Copyright 2024 Nomios UK&I

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import typing as t

from yapyang.constants import DEFAULTS, XML_ATTRIBUTE_TEMPLATE, UNSET

__all__ = ("MetaInfo",)


class MetaInfo:
    """YANG data model metadata information."""

    def __init__(
        self,
        default: t.Any = UNSET,
        attrs: t.Optional[t.Dict[str, str]] = None,
    ) -> None:
        self.default = default
        self.attrs = attrs


def concatenate_xml_element_attrs(attrs: t.Optional[t.Dict[str, str]]) -> str:
    """Concatenates XML element attributes."""

    element_attrs: str = ""
    if attrs:
        for attr, value in attrs.items():
            element_attrs += XML_ATTRIBUTE_TEMPLATE.format(attr, value)

    return element_attrs


def retrieve_xml_element_attrs(
    cls_meta: t.Dict[str, t.Any], cls_arg: str, /
) -> t.Optional[dict]:
    """Retrieves XML element attributes from class meta for class arg."""

    if cls_attr_default := cls_meta[DEFAULTS].get(cls_arg):
        if isinstance(cls_attr_default, MetaInfo):
            return cls_attr_default.attrs

    return None
