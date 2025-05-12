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

from ordered_set import OrderedSet

from yapyang.constants import (
    ANNOTATIONS,
    ARGS,
    DEFAULTS,
    IDENTIFIER,
    UNSET,
    XML_ELEMENT_TEMPLATE,
)
from yapyang.utils import (
    MetaInfo,
    concatenate_xml_element_attrs,
    retrieve_xml_element_attrs,
)

__all__ = (
    "ModuleNode",
    "ContainerNode",
    "ListNode",
    "LeafListNode",
    "LeafNode",
)


class NodeMeta(type):
    """Metaclass for all YANG nodes."""

    @staticmethod
    def _construct_meta(namespace: dict, bases: tuple, /) -> None:
        """Constructs namespace metadata from type annotations."""

        metadata: t.Dict[str, t.Any] = dict()
        args: t.Dict[str, t.Type[t.Any]] = dict()
        defaults: t.Dict[str, t.Any] = dict()

        # Inherit from parents (bases) meta.
        for base_meta in [base.__meta__ for base in bases[::-1]]:
            # Reverse so that leftmost base overwrites right.
            metadata.update(base_meta)
            args.update(base_meta[ARGS])
            defaults.update(base_meta[DEFAULTS])

        # Override parents (bases) meta with namespace.
        if namespace_annotations := namespace.pop(ANNOTATIONS, None):
            for attr, annotation in namespace_annotations.items():
                if attr.startswith("__") and attr.endswith("__"):
                    metadata[attr] = annotation
                else:
                    args[attr] = annotation

        for attr in list(namespace):
            if attr in metadata or attr in args:
                defaults[attr] = namespace.pop(attr)

        metadata[ARGS] = args
        metadata[DEFAULTS] = defaults
        namespace["__meta__"] = metadata

    @staticmethod
    def _check_meta(cls_name: str, metadata: dict, /) -> None:
        """Ensures that YANG node is valid."""

        if cls_name in (
            "Node",
            "InitNode",
            "ModuleNode",
            "ContainerNode",
            "ListNode",
            "LeafListNode",
            "LeafNode",
        ):
            return

        if metadata[IDENTIFIER] is not str:
            raise TypeError(f"Changing {IDENTIFIER} annotation is forbidden.")
        if IDENTIFIER not in metadata[DEFAULTS]:
            metadata[DEFAULTS][IDENTIFIER] = cls_name.lower()

    def __new__(cls, cls_name: str, bases: tuple, namespace: dict):
        """Constructs class namespace metadata, and creates class object."""

        cls._construct_meta(namespace, bases)
        cls._check_meta(cls_name, namespace["__meta__"])
        return super().__new__(cls, cls_name, bases, namespace)


class Node(metaclass=NodeMeta):
    """Base class for all YANG nodes."""

    __identifier__: str

    def __init__(self) -> None:
        """Initializer that creates the mechanics for expected behavior."""

        self._cls_meta: t.Dict[str, t.Any] = self.__class__.__meta__  # type: ignore
        self._cls_identifier: str = self._cls_meta[DEFAULTS][IDENTIFIER]

    def __new__(cls, *args, **kwargs):
        """Prevents instances of Node or direct subclasses."""

        if cls is Node or cls in Node.__subclasses__():
            raise TypeError(
                "Node or subclasses of cannot be directly instantiated."
            )
        return super().__new__(cls)

    def _resolve_cls_meta_args(
        self, args: tuple, kwargs: dict
    ) -> t.Generator[t.Tuple[str, t.Any], None, None]:
        """Yields the name and resolved value for each class meta
        argument."""

        self._check_given_args_not_greater_than_expected(
            (len(args) + len(kwargs))
        )
        for index, cls_arg in enumerate(self._cls_meta[ARGS]):
            value = UNSET
            if len(args) > index:
                value = args[index]
            elif cls_arg in kwargs:
                value = kwargs[cls_arg]
            elif cls_arg in self._cls_meta[DEFAULTS]:
                if (
                    type((value := self._cls_meta[DEFAULTS][cls_arg]))
                    is MetaInfo
                ):
                    value = value.default
            if value is UNSET:
                raise TypeError(f"Missing required argument: {cls_arg}")
            yield (cls_arg, value)

    def _check_given_args_not_greater_than_expected(self, given: int) -> None:
        """Checks the number of given arguments does not exceed the
        number of class meta arguments."""

        if given > (expected := len(self._cls_meta[ARGS])):
            raise TypeError(
                f"{self.__class__.__name__} takes {expected} arguments, but {given} were given."
            )


class InitNode(Node):
    """Base class for YANG nodes that initialize with args."""

    def __init__(self, *args, **kwargs) -> None:
        """Initializer that takes any number of arguments for class meta
        args."""

        super().__init__()
        for cls_arg, value in self._resolve_cls_meta_args(args, kwargs):
            setattr(self, cls_arg, value)


class ModuleNode(InitNode, Node):
    """Base class for YANG module node."""

    __namespace__: str

    def to_xml(self) -> str:
        """Returns an XML tree from instance."""

        xml_tree: str = ""
        for cls_arg in self._cls_meta[ARGS]:
            attrs: dict = dict(xmlns=self._cls_meta[DEFAULTS]["__namespace__"])
            if element_attrs := retrieve_xml_element_attrs(
                self._cls_meta, cls_arg
            ):
                attrs.update(element_attrs)
            xml_tree += getattr(self, cls_arg).to_xml(attrs=attrs)

        return xml_tree


class ContainerNode(InitNode, Node):
    """Base class for YANG container node."""

    def to_xml(self, /, *, attrs: t.Optional[t.Dict[str, str]] = None) -> str:
        """Returns an XML tree from instance element. When attrs are
        provided instance element contains attrs."""

        element_attrs = concatenate_xml_element_attrs(attrs)
        element_value: str = ""
        for cls_arg in self._cls_meta[ARGS]:
            element_value += getattr(self, cls_arg).to_xml(
                attrs=retrieve_xml_element_attrs(self._cls_meta, cls_arg)
            )

        return XML_ELEMENT_TEMPLATE.format(
            self._cls_identifier, element_attrs, element_value
        )


class ListEntry:
    """Base class for YANG list node entry."""

    def __init__(self, attributes: t.Dict[str, t.Any], /, *, key: str) -> None:
        """Initializer that manifests into entry through attributes."""

        self.__dict__.update(attributes)
        self._key = key

    def __hash__(self):
        """Returns hash of entry from key values."""

        return hash(
            tuple((self.__dict__[key] for key in self._key.split(",")))
        )


class ListNode(Node):
    """Base class for YANG list node."""

    __key__: str

    def __init__(self) -> None:
        """Initializer that creates the mechanics for expected behavior."""

        super().__init__()
        self.entries: OrderedSet = OrderedSet()
        self._key: str = self._cls_meta[DEFAULTS]["__key__"]

    def append(self, *args, **kwargs) -> None:
        """Takes any number of arguments for class meta args to append a
        new entry into list entries.
        """

        entry_attr: t.Dict[str, t.Any] = dict()
        for cls_arg, value in self._resolve_cls_meta_args(args, kwargs):
            entry_attr[cls_arg] = value
        self.entries.add(ListEntry(entry_attr, key=self._key))

    def to_xml(self, /, *, attrs: t.Optional[t.Dict[str, str]] = None) -> str:
        """Returns an XML tree from each entries element. When attrs are
        provided each entry element contains attrs."""

        element_attrs = concatenate_xml_element_attrs(attrs)
        xml_tree: str = ""
        for entry in self.entries:
            element_value: str = ""
            for cls_arg in self._cls_meta[ARGS]:
                element_value += getattr(entry, cls_arg).to_xml(
                    attrs=retrieve_xml_element_attrs(self._cls_meta, cls_arg)
                )
            xml_tree += XML_ELEMENT_TEMPLATE.format(
                self._cls_identifier, element_attrs, element_value
            )

        return xml_tree


class LeafListNode(Node):
    """Base class for YANG leaf list node."""

    value: t.Any

    def __init__(self) -> None:
        """Initializer that creates the mechanics for expected behavior."""

        super().__init__()
        self.entries: OrderedSet = OrderedSet()

    def append(self, *value) -> None:
        """Takes a single ;) value argument to append a new entry into leaf
        list entries.
        """

        for _, value in self._resolve_cls_meta_args(value, dict()):
            self.entries.add(value)

    def to_xml(self, /, *, attrs: t.Optional[t.Dict[str, str]] = None) -> str:
        """Returns XML element for each entry. When attrs are provided
        each entry element contains attrs."""

        element_attrs = concatenate_xml_element_attrs(attrs)
        elements: str = ""
        for element_value in self.entries:
            elements += XML_ELEMENT_TEMPLATE.format(
                self._cls_identifier, element_attrs, element_value
            )

        return elements


class LeafNode(InitNode, Node):
    """Base class for YANG leaf node."""

    value: t.Any

    def to_xml(self, /, *, attrs: t.Optional[t.Dict[str, str]] = None) -> str:
        """Returns XML from instance element. When attrs are
        provided instance element contains attrs."""

        element_attrs = concatenate_xml_element_attrs(attrs)
        return XML_ELEMENT_TEMPLATE.format(
            self._cls_identifier,
            element_attrs,
            getattr(self, *self._cls_meta[ARGS].keys()),
        )
