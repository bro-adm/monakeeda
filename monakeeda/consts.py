class PythonNamingConsts:
    annotations = '__annotations__'
    CONFIG = 'Config'


class NamespacesConsts:
    COMPONENTS = '__monkey_components__'
    STRUCT = '__monkey_struct__'
    EXCEPTIONS = '__monkey_exceptions__'

    FIELDS = 'fields'
    ANNOTATIONS = 'annotations'
    DECORATORS = 'decorators'
    CONFIG = 'config'


class FieldConsts:
    FIELD = 'field'
    REQUIRED = 'required'
    TYPE = 'type'
    ANNOTATION = 'annotation_cls'
    VALIDATORS = 'validators'
    CREATOR = 'creator'
    DEPENDENTS = 'dependents'
    DEPENDENCIES = 'dependencies'
    VALUE = 'value'


class ConfigConsts:
    OBJECT = 'object'


class DecoratorConsts:
    DECORATED_WITH = '__decorated_with__'  # model methods decorators instances space
