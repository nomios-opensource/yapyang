"""This module contains YANG nodes."""

ANNOTATIONS: str = "__annotations__"


class NodeMeta(type):
    @staticmethod
    def _construct_metadata(namespace: dict, bases: tuple, /) -> None:
        """Constructs namespace metadata from type annotations."""

        defaults = dict()
        annotations = dict()

        for base_metadata in [base.__metadata__ for base in bases[::-1]]:
            if base_metadata_annotations := base_metadata[ANNOTATIONS]:
                annotations |= base_metadata_annotations
            defaults |= base_metadata

        if namespace_annotations := namespace.pop(ANNOTATIONS, None):
            annotations |= namespace_annotations
        for attr in list(namespace.keys()):
            if attr in annotations:
                defaults[attr] = namespace.pop(attr)

        defaults[ANNOTATIONS] = annotations
        namespace["__metadata__"] = defaults

    def __new__(meta_cls, cls_name: str, bases: tuple, namespace: dict):
        """Converts type annotated class attributes to instance."""

        meta_cls._construct_metadata(namespace, bases)
        return super().__new__(meta_cls, cls_name, bases, namespace)


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
