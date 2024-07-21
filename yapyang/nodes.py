"""This module contains YANG nodes."""

import typing as t

from ordered_set import OrderedSet

ANNOTATIONS: str = "__annotations__"


class NodeMeta(type):
    """Metaclass for all YANG nodes."""

    @staticmethod
    def _construct_metadata(namespace: dict, bases: tuple, /) -> None:
        """Constructs namespace metadata from type annotations."""

        defaults: dict[str, t.Any] = dict()
        annotations: dict[str, type[t.Any]] = dict()

        # Inherit from parents (bases) metadata.
        for base_metadata in [base.__metadata__ for base in bases[::-1]]:
            annotations |= base_metadata[ANNOTATIONS]
            defaults |= base_metadata

        # Override parents (bases) metadata with namespace.
        if namespace_annotations := namespace.pop(ANNOTATIONS, None):
            annotations |= namespace_annotations
        for attr in list(namespace.keys()):
            if attr in annotations:
                defaults[attr] = namespace.pop(attr)

        defaults[ANNOTATIONS] = annotations
        namespace["__metadata__"] = defaults

    def __new__(cls, cls_name: str, bases: tuple, namespace: dict):
        """Constructs class namespace metadata, and creates class object."""

        cls._construct_metadata(namespace, bases)
        return super().__new__(cls, cls_name, bases, namespace)


class Node(metaclass=NodeMeta):
    """Base class for all YANG nodes."""

    identifier: t.Optional[str] = None

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        """Initializer that takes any number of arguments for annotated
        class attributes."""

        cls_metadata: dict[str, t.Any] = self.__class__.__metadata__

        # Checks that number of args and kwargs does not exceed the
        # number of annotated class attributes.
        if (got := len(args) + len(kwargs)) > (
            expected := len(cls_metadata[ANNOTATIONS])
        ):
            raise TypeError(
                f"{self.__class__.__name__} takes {expected} arguments, but {got} were given."
            )

        for index, attr in enumerate(cls_metadata[ANNOTATIONS]):
            if len(args) > index:
                value = args[index]
            elif attr in kwargs:
                value = kwargs[attr]
            elif attr in cls_metadata:
                value = cls_metadata[attr]
            else:
                raise TypeError(f"Missing required argument: {attr}")

            setattr(self, attr, value)

    def __new__(cls, *args: tuple, **kwargs: dict):
        """Prevents instances of Node or direct subclasses."""

        if cls is Node or cls in Node.__subclasses__():
            raise TypeError(
                "Node or subclasses of cannot be directly instantiated."
            )
        return super().__new__(cls)


class ModuleNode(Node):
    """Base class for YANG module node."""

    namespace: t.Optional[str] = None


class ContainerNode(Node):
    """Base class for YANG container node."""


class ListEntry:
    """Base class for YANG list node entry."""

    def __init__(self, attributes: dict[str, t.Any], /, *, key: str) -> None:
        """Initializer that manifests into entry through attributes."""

        self.__dict__ |= attributes
        self._key = key

    def __hash__(self):
        """Returns hash of entry from key values."""

        return hash(
            tuple((self.__dict__[key] for key in self._key.split(",")))
        )


class ListNode(Node):
    """Base class for YANG list node."""

    key: str

    def __init__(self) -> None:
        self.entries: OrderedSet = OrderedSet()
        self._cls_metadata = self.__class__.__metadata__
        self._key = self._cls_metadata["key"]

    def append(self, *args, **kwargs) -> None:
        """Takes any number of arguments for annotated class attributes
        to append a new entry into list entries.
        """

        # Checks that number of args and kwargs does not exceed the
        # number of annotated class attributes.
        if (got := len(args) + len(kwargs)) > (
            expected := len(list(self._cls_metadata[ANNOTATIONS])[2:])
        ):
            raise TypeError(
                f"{self.__class__.__name__} takes {expected} arguments, but {got} were given."
            )

        entry_attr: dict[str, t.Any] = dict()
        for index, attr in enumerate(
            list(self._cls_metadata[ANNOTATIONS])[2:]
        ):
            if len(args) > index:
                value = args[index]
            elif attr in kwargs:
                value = kwargs[attr]
            elif attr in self._cls_metadata:
                value = self._cls_metadata[attr]
            else:
                raise TypeError(f"Missing required argument: {attr}")
            entry_attr[attr] = value
        self.entries.add(ListEntry(entry_attr, key=self._key))


class LeafListNode(Node):
    """Base class for YANG leaf list node."""


class LeafNode(Node):
    """Base class for YANG leaf node."""
