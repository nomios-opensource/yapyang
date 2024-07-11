"""This module contains YANG nodes."""

import typing as t

ANNOTATIONS: str = "__annotations__"


class NodeMeta(type):
    @staticmethod
    def _construct_metadata(namespace: dict, bases: tuple, /) -> None:
        """Constructs namespace metadata from type annotations."""

        defaults: dict[str, t.Any] = dict()
        annotations: dict[str, type[t.Any]] = dict()

        for base_metadata in [base.__metadata__ for base in bases[::-1]]:
            annotations |= base_metadata[ANNOTATIONS]
            defaults |= base_metadata

        if namespace_annotations := namespace.pop(ANNOTATIONS, None):
            annotations |= namespace_annotations
        for attr in list(namespace.keys()):
            if attr in annotations:
                defaults[attr] = namespace.pop(attr)

        defaults[ANNOTATIONS] = annotations
        namespace["__metadata__"] = defaults

    def __new__(cls, cls_name: str, bases: tuple, namespace: dict):
        """Converts type annotated class attributes to instance."""

        cls._construct_metadata(namespace, bases)
        return super().__new__(cls, cls_name, bases, namespace)


class Node(metaclass=NodeMeta):
    identifier: str


class ModuleNode(Node):
    namespace: str


class ContainerNode(Node):
    pass


class ListNode(Node):
    pass


class LeafListNode(Node):
    pass


class LeafNode(Node):
    pass
