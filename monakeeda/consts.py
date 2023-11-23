class PythonNamingConsts:
    annotations = '__annotations__'


class ComponentConsts:
    FIELD_KEY = '_field_key'
    GLOBAL = 'global'


class NamespacesConsts:
    COMPONENTS = '__monkey_components__'
    STRUCT = '__monkey_struct__'
    TMP = '__monkey_tmp__'

    FIELDS = 'fields'
    ANNOTATIONS = 'annotations'
    DECORATORS = 'decorators'
    CONFIGS = 'configs'
    DISCRIMINATOR = 'discriminator'


class FieldConsts:
    FIELD = 'field'
    REQUIRED = 'required'
    PRIVATE = 'private'
    ANNOTATION = 'annotation_cls'
    VALIDATORS = 'validators'
    CREATOR = 'creator'
    MUTATORS = 'mutators'
    DEPENDENTS = 'dependents'
    DEPENDENCIES = 'dependencies'
    COMPONENTS = 'components'


class ConfigConsts:
    OBJECT = 'object'
    COMPONENTS = 'components'


class DecoratorConsts:
    DECORATED_WITH = '__decorated_with__'  # model methods decorators instances space


class TmpConsts:
    GENERICS = 'generics'


class DiscriminationConsts:
    FIELD_KEY = 'field_key'
    VALUES = 'values'
