from functools import reduce
from typing import List, Tuple

from .scope_dict import ScopesDict


def extract_main_scope(scope: str):
    return scope.split('.', 1)[0]


def compare_scopes(scope1: str, scope2: str):
    scope1_main = extract_main_scope(scope1)
    scope2_main = extract_main_scope(scope2)

    return scope1_main == scope2_main


def extract_all_components_of_main_scope(scopes: ScopesDict, main_scope: str) -> Tuple[List[str], List['Component']]:
    scopes_keys = scopes.keys()

    relevant_scopes = [scope_key for scope_key in scopes_keys if extract_main_scope(scope_key) == main_scope]
    scoped_components = [reduce(lambda x1, x2: [*x1, *x2], scopes[scope].values(), []) for scope in relevant_scopes]
    components = list(reduce(lambda x1, x2: [*x1, *x2], scoped_components, []))

    return relevant_scopes, components
