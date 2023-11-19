from collections import OrderedDict
from typing import List, TypeVar

from monakeeda.consts import NamespacesConsts, PythonNamingConsts, TmpConsts
from .base_annotations import Annotation
from ..meta import ComponentManager


class AnnotationManager(ComponentManager):
    """
    The Annotations concept allows for multiple Annotations implementations, BUT one per type.
    The type to annotation mapping is overrideable via an annotations mapper or directly on the passed annotation mapping.

    The Annotations Manager responsibility, just like most other Component Manager is to find the relevant components, build them
    and manage inheritance collisions.

    Here collisions arent hard at all due to not having sub components - on collision make arbitrary type.

    attrs must be configured with an annotation directly - but not always a Monakeeda Annotation.
    attrs are provided either a Monakeeda Annotation or a python native annotation (e.g. str)

    Either way, this Manager needs to get the mapped Monakeeda Annotation from the given one and initialize it.
    """

    def __init__(self, annotation_mapping):
        self._annotation_mapping = annotation_mapping

    def _components(self, monkey_cls) -> List[Annotation]:
        return getattr(monkey_cls, NamespacesConsts.STRUCT)[NamespacesConsts.ANNOTATIONS].values()

    def _find_field_by_type_var(self, monkey_cls, type_var: TypeVar) -> str:
        for field_key, annotation_instance in monkey_cls.struct[NamespacesConsts.ANNOTATIONS].items():
            if annotation_instance.base_type == type_var:
                return field_key

    def _set_by_base(self, monkey_cls, base, attrs, collisions):
        _ObjectAnnotation = self._annotation_mapping[object]

        current_annotations_keys = set(attrs[NamespacesConsts.STRUCT][NamespacesConsts.ANNOTATIONS].keys())  # prior bases merged set of fields
        base_annotations_keys = set(base.struct[NamespacesConsts.ANNOTATIONS].keys())  # current base set of fields

        collided_fields = current_annotations_keys & base_annotations_keys  # intersection
        for field_key in collided_fields:
            # No valdiations needs to happen -> if there are collision at all -> the annotation will be set as Arbitrary Object
            # Note that this means that we dont need to update or check the collisions parameter because collisions will keep on happening on next bases without it

            object_annotations = _ObjectAnnotation(field_key, object, self._annotation_mapping)

            attrs[NamespacesConsts.STRUCT][NamespacesConsts.ANNOTATIONS][field_key] = object_annotations

        new_fields_keys = base_annotations_keys - current_annotations_keys
        for new_field_key in new_fields_keys:
            new_annotation = base.struct[NamespacesConsts.ANNOTATIONS][new_field_key]
            monkey_cls.struct[NamespacesConsts.ANNOTATIONS][new_field_key] = new_annotation

        base_tmp = getattr(base, NamespacesConsts.TMP)
        if TmpConsts.GENERICS in base_tmp:
            updated_wanted_generics = base_tmp[TmpConsts.GENERICS]  # provided generics for model - either new TypeVar or an actual type
            model_generics = base.__parameters__  # saved attr for Generics -> saved in tuple which preserves order -> instantiated TypeVars

            updated_generics_amount = len(updated_wanted_generics)

            for i in range(updated_generics_amount):
                # the data structures in which they are provided keep their order
                updated_wanted_generic = updated_wanted_generics[i]
                model_generic = model_generics[i]

                field_key = self._find_field_by_type_var(monkey_cls, model_generic)
                self._annotation_mapping[updated_wanted_generic]
                annotation_cls_instance = self._annotation_mapping[updated_wanted_generic](field_key, updated_wanted_generic, self._annotation_mapping)
                attrs[NamespacesConsts.STRUCT][NamespacesConsts.ANNOTATIONS][field_key] = annotation_cls_instance

    def _set_curr_cls(self, monkey_cls, bases, monkey_attrs):
        annotations = monkey_attrs.get(PythonNamingConsts.annotations, {})  # shouldn't be {}

        for key, annotation in annotations.items():
            self._annotation_mapping[annotation]

            annotation_cls_instance = self._annotation_mapping[annotation](key, annotation, self._annotation_mapping)
            monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.ANNOTATIONS][key] = annotation_cls_instance

    def build(self, monkey_cls, bases, monkey_attrs):
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.ANNOTATIONS] = OrderedDict()
        super(AnnotationManager, self).build(monkey_cls, bases, monkey_attrs)
