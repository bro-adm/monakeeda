import logging
from typing import Optional, Union, List

from monakeeda import *
from monakeeda.logger import logger, MonkeyLogHandler

logger.setLevel(logging.DEBUG)

handler = MonkeyLogHandler(log=True)
logger.addHandler(handler)

log_main_information()

print(OptionalAnnotation.__managed_components__)
print(UnionAnnotation.__managed_components__)
print(Discriminator.__managed_components__)
print(NumericTypeAnnotation.__managed_components__)


class Main(MonkeyModel):
    # c: Optional[Const[int]] = Field(gt=9)
    # a: Optional[Union[str, int]]
    a: Union[Const[str], Positive[int]] = Field(lt=8)
    # a: Union[Negative[int], Positive[int], str] = Field(lt=8, gt=-50)
    # a: Union[str, Positive[int]] = Field(lt=8, gt=-50)
    # b: List[int] = Field(gt=9)

    # @Validator('a')
    # def validate_a(self, *_, **__):
    #     print("inside validator")

# m = Main(a=-100, b=[1,"2","3"], c=-6)
# m = Main(a=7)
# m.a = 5

m = Main(a="bro")
m.a = "lol"

# print(m.__dict__['a'])
print(m.__run_organized_components__)
# print(Main.__run_organized_components__)
