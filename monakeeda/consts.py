class PythonNamingConsts:
    annotations = '__annotations__'


class NamespacesConsts:
    BUILD = 'build'
    EXCEPTIONS = 'exceptions'
    DECORATORS = 'decorators'
    FIELDS = 'fields_info'  # TODO: validate if can change to 'fields'
    FIELDS_KEYS = 'main_field_keys'  # TODO: validate if can get rid of this
    ANNOTATIONS = 'annotations'

    DECORATED_WITH = '__decorated_with__'  # model methods decorators instances space


class FieldConsts:
    FIELD = 'field'
    REQUIRED = 'required'
    TYPE = 'type'
    ANNOTATION = 'annotation_cls'
