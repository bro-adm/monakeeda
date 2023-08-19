from typing import List

from monakeeda.consts import NamespacesConsts, ConfigConsts
from monakeeda.helpers import get_cls_attrs
from .base_config import Config
from ..component import MainComponent

"""
class A(MonkeyModel):
    a: int
    
    class Config(Config):
        x = 1
        
class B(A):
    b: int
    
    class Config(Config):
        y = 2
        
class C(A):
    c: int
    
    class Config(A.Config):
        y = 3
        
!!! NO MATTER OPTION B OR C BECAUSE WHEN THE MODEL ITSELF INHERITS FROM A ALL THE CLASS MAPPINGS OF A ARE PASSED 
THROUGH INCLUDING THOSE THAT HAPPENED BECAUSE OF THE CONFIG CLASS PARAMETERS SO IN ORDER TO NEGATE WHAT HAPPENS IN THE 
FATHER MODEL CONFIG CLASS U NEED TO CREATE A CONFIG CLASS IN THE CURRENT MODEL WITH THE NEGATIVE PARAMETER VALUES 
U WANT TO NEGATE !!!  
"""


class ConfigMainComponent(MainComponent[Config]):

    def _components(self, monkey_cls) -> List[Config]:
        return [monkey_cls.__map__[NamespacesConsts.BUILD][NamespacesConsts.CONFIG]]

    def _set_by_base(self, monkey_cls, base, attrs):
        """
        The effects of all the configurations in prior bases already effected their namespaces
        which will be taken into account by prior configurations taking place
        """

        pass

    def _set_curr_cls(self, monkey_cls, bases, monkey_attrs):
        monkey_cls_config = getattr(monkey_cls, ConfigConsts.CONFIG)
        monkey_cls_config_attrs = get_cls_attrs(monkey_cls_config)

        initialized_config: Config = monkey_cls_config(**monkey_cls_config_attrs)
        monkey_cls.__map__[NamespacesConsts.BUILD][NamespacesConsts.CONFIG] = initialized_config
