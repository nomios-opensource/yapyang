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
