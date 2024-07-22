"""This module contains YANG nodes."""

import typing as t

from ordered_set import OrderedSet

ANNOTATIONS: str = "__annotations__"
META: str = "__meta__"
ARGS: str = "__args__"
DEFAULTS: str = "__defaults__"


class NodeMeta(type):
    """Metaclass for all YANG nodes."""

    @staticmethod
    def _construct_meta(namespace: dict, bases: tuple, /) -> None:
        """Constructs namespace metadata from type annotations."""

        metadata: dict[str, t.Any] = dict()
        args: dict[str, type[t.Any]] = dict()
        defaults: dict[str, t.Any] = dict()

        # Inherit from parents (bases) meta.
        for base_meta in [base.__meta__ for base in bases[::-1]]:
            metadata |= base_meta
            args |= base_meta[ARGS]
            defaults |= base_meta[DEFAULTS]

        # Override parents (bases) meta with namespace.
        if namespace_annotations := namespace.pop(ANNOTATIONS, None):
            for attr, annotation in namespace_annotations.items():
                if attr.startswith("__") and attr.endswith("__"):
                    metadata[attr] = annotation
                else:
                    args[attr] = annotation

        for attr in list(namespace.keys()):
            if attr in metadata or attr in args:
                defaults[attr] = namespace.pop(attr)

        metadata[ARGS] = args
        metadata[DEFAULTS] = defaults
        namespace["__meta__"] = metadata

    def __new__(cls, cls_name: str, bases: tuple, namespace: dict):
        """Constructs class namespace metadata, and creates class object."""

        cls._construct_meta(namespace, bases)
        return super().__new__(cls, cls_name, bases, namespace)


class Node(metaclass=NodeMeta):
    """Base class for all YANG nodes."""

    __identifier__: t.Optional[str] = None

    def __init__(self, *args, **kwargs) -> None:
        """Initializer that takes any number of arguments for class meta
        args."""

        cls_meta: dict[str, t.Any] = self.__class__.__meta__

        # Checks that number of args and kwargs does not exceed the
        # number of class meta args.
        if (got := len(args) + len(kwargs)) > (
            expected := len(cls_meta[ARGS])
        ):
            raise TypeError(
                f"{self.__class__.__name__} takes {expected} arguments, but {got} were given."
            )

        for index, attr in enumerate(cls_meta[ARGS]):
            if len(args) > index:
                value = args[index]
            elif attr in kwargs:
                value = kwargs[attr]
            elif attr in cls_meta[DEFAULTS]:
                value = cls_meta[DEFAULTS][attr]
            else:
                raise TypeError(f"Missing required argument: {attr}")

            setattr(self, attr, value)

    def __new__(cls, *args, **kwargs):
        """Prevents instances of Node or direct subclasses."""

        if cls is Node or cls in Node.__subclasses__():
            raise TypeError(
                "Node or subclasses of cannot be directly instantiated."
            )
        return super().__new__(cls)


class ModuleNode(Node):
    """Base class for YANG module node."""

    __namespace__: t.Optional[str] = None


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

    __key__: str

    def __init__(self) -> None:
        self.entries: OrderedSet = OrderedSet()
        self._cls_meta = self.__class__.__meta__
        self._key = self._cls_meta[DEFAULTS]["__key__"]

    def append(self, *args, **kwargs) -> None:
        """Takes any number of arguments for class meta args to append a
        new entry into list entries.
        """

        # Checks that number of args and kwargs does not exceed the
        # number of class meta args.
        if (got := len(args) + len(kwargs)) > (
            expected := len(self._cls_meta[ARGS])
        ):
            raise TypeError(
                f"{self.__class__.__name__} takes {expected} arguments, but {got} were given."
            )

        entry_attr: dict[str, t.Any] = dict()
        for index, attr in enumerate(self._cls_meta[ARGS]):
            if len(args) > index:
                value = args[index]
            elif attr in kwargs:
                value = kwargs[attr]
            elif attr in self._cls_meta[DEFAULTS]:
                value = self._cls_meta[DEFAULTS][attr]
            else:
                raise TypeError(f"Missing required argument: {attr}")
            entry_attr[attr] = value
        self.entries.add(ListEntry(entry_attr, key=self._key))


class LeafListNode(Node):
    """Base class for YANG leaf list node."""


class LeafNode(Node):
    """Base class for YANG leaf node."""
