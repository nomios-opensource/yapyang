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

__all__ = ()

ANNOTATIONS: str = "__annotations__"
META: str = "__meta__"
ARGS: str = "__args__"
DEFAULTS: str = "__defaults__"

# None equals YANG type empty, therefore a sentinel object is required.
UNSET: object = object()

XML_ELEMENT_TEMPLATE: str = "<{0}{1}>{2}</{0}>"
XML_ATTRIBUTE_TEMPLATE: str = ' {0}="{1}"'

IDENTIFIER: str = "__identifier__"
