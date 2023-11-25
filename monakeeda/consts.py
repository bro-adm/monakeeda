class PythonNamingConsts:
    annotations = '__annotations__'


class NamespacesConsts:
    COMPONENTS = '__monkey_components__'
    STRUCT = '__monkey_struct__'
    SCOPES = '__monkey_scopes__'
    TMP = '__monkey_tmp__'

    FIELDS = 'fields'
    ANNOTATIONS = 'annotations'
    DECORATORS = 'decorators'
    CONFIGS = 'configs'


class FieldConsts:
    FIELD = 'field'
    REQUIRED = 'required'
    PRIVATE = 'private'
    DEPENDENTS = 'dependents'
    DEPENDENCIES = 'dependencies'


class ConfigConsts:
    OBJECT = 'object'


class DecoratorConsts:
    DECORATED_WITH = '__monkey_decorated_with__'  # model methods decorators instances space


class TmpConsts:
    GENERICS = 'generics'
