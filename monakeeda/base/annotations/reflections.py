from collections import defaultdict

from .base_annotations import GenericAnnotation


def map_annotations(annotation: GenericAnnotation, base_types=False) -> dict:
    map = defaultdict(lambda: [], {})

    sub_annotations = annotation._annotations
    for sub_annotation in sub_annotations:
        if isinstance(sub_annotation, GenericAnnotation):
            map.update(map_annotations(sub_annotation, base_types))
        else:
            map[annotation].append(sub_annotation.base_type)

    return map
