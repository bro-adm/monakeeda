from collections import OrderedDict
from typing import List

from monakeeda.consts import NamespacesConsts, PythonNamingConsts
from .base_annotation import Annotation
from ..component import MainComponent


class AnnotationMainComponent(MainComponent[Annotation]):
    def __init__(self, annotation_mapping):
        self._annotation_mapping = annotation_mapping

    def _components(self, monkey_cls) -> List[Annotation]:
        return monkey_cls.__map__[NamespacesConsts.BUILD][NamespacesConsts.ANNOTATIONS].values()

    def _set_by_base(self, monkey_cls, base, monkey_attrs):
        monkey_cls.__map__[NamespacesConsts.BUILD][NamespacesConsts.ANNOTATIONS].\
            update(base.__map__[NamespacesConsts.BUILD][NamespacesConsts.ANNOTATIONS])

    def _set_curr_cls(self, monkey_cls, bases, monkey_attrs):
        annotations = monkey_attrs.get(PythonNamingConsts.annotations, {})  # shouldn't be {}

        for key, annotation in annotations.items():
            annotation_cls = self._annotation_mapping[annotation]
            monkey_cls.__map__[NamespacesConsts.BUILD][NamespacesConsts.ANNOTATIONS][key] = annotation_cls
            # TODO: validate if custom namespace required for annotations instead of reading from fields

    def run_bases(self, monkey_cls, bases, monkey_attrs):
        monkey_cls.__map__[NamespacesConsts.BUILD].setdefault(NamespacesConsts.ANNOTATIONS, OrderedDict())
        super(AnnotationMainComponent, self).run_bases(monkey_cls, bases, monkey_attrs)
