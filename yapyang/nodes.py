"""This module contains YANG nodes."""

import typing as t

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

    def __init__(self, *args, **kwargs) -> None:
        """Initializer that takes any number of arguments for annotated
        class attributes."""

        cls_metadata: dict[str, t.Any] = self.__class__.__metadata__  # type: ignore

        # Checks that number of args and kwargs does not exceed the
        # number of annotated class attributes.
        if (got := len(args) + len(kwargs)) > (
            expected := len(cls_metadata[ANNOTATIONS])
        ):
            raise TypeError(
                f"{self.__class__.__name__} takes {expected} arguments, but {got} were given."
            )

        for index, (name, annotation) in enumerate(
            cls_metadata[ANNOTATIONS].items()
        ):
            if len(args) > index:
                setattr(self, name, args[index])
            elif name in kwargs:
                setattr(self, name, kwargs[name])
            elif name in cls_metadata:
                setattr(self, name, cls_metadata[name])
            else:
                raise TypeError(f"Missing required argument: {name} ")


class ContainerNode(Node):
    """Base class for YANG container node."""

    pass


class ListNode(Node):
    """Base class for YANG list node."""

    pass


class LeafListNode(Node):
    """Base class for YANG leaf list node."""

    pass


class LeafNode(Node):
    """Base class for YANG leaf node."""

    pass
