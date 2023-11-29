from .scope_dict import ScopeDict, ScopesDict
from .helpers import extract_main_scope, compare_scopes, extract_all_components_of_main_scope

"""
Multiple components can have the same scope.
There are global scopes like ValidateMissingFields (values_managers) and FileInputConfigParameter (values_provider).
There a field level scopes -> field_key

There are labels for each component and our want it to group together all component under a same scope&label.
multiple components under the scope&label combo run the is_collision api between them to raise build error if illegal.

That being said, there are components that aren't always supposed to be run.
They are flagged prior to being added to the scopes namespace.

They are flagged via setting their scope as prior_scope.path...
e.g. Union[int, str] -> Union will keep the main scope, while int and str will look -> main.Union:0, main.Union:1

That happens at first in order for managed subcomponents to not collide with one another at label collision validation.
Then it happens in order for them (if managers) to copy-update managing components to their new scope for later label collison validations.

This dict is also used to get all the components under a scope.
Because we have plausible scopes if you can ask for scopes under main and receive all components under main and all its subpaths.

Do remember that subpath components are silent on runs unless toggled to run on runtime and therefore always managed.
Unmanaged types that should be managed do not add themselves to scope.

key = label
value = list of components
"""

