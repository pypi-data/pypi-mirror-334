from anygrad.utils import utils_c as C
from anygrad.tensor.base import ThHelper as Th
from anygrad.tensor.tensor import Tensor
import random


class Generator(C.GeneratorBase):
    def __init__(self, seed):
        super().__init__(seed)

    def manual_seed(self, seed):
        return super().manual_seed(seed)
    
    __module__ = "anygrad"


def _use_utils_ops(operation_name, dtype, **kwargs):

    if isinstance(kwargs["shape"][0], tuple) and len(kwargs["shape"]) == 1:
        kwargs["shape"] = kwargs["shape"][0]

    dtype_mapping = {
        Th.float32: "float32",
        Th.float64: "float64",
        Th.int32: "int32",
        Th.int64: "int64",
    }
    try:
        operation_func = getattr(
            C, f"{operation_name.capitalize()}{dtype_mapping[dtype].capitalize()}"
        )
    except Exception:
        pass

    if "low" in kwargs:
        data, shape = operation_func(
            kwargs["shape"], kwargs["low"], kwargs["high"], kwargs["generator"]
        )
    else:
        data, shape = operation_func(kwargs["shape"], kwargs["generator"])
    ans = Th.reshape(data, shape)
    del data, shape
    ans = Tensor(ans, kwargs["requires_grad"], dtype=dtype_mapping[dtype])
    return ans


def rand(*shape, generator=None, requires_grad=False, dtype=Th.float32):
    if dtype not in {Th.float32, Th.float64}:
        raise TypeError(
            "In valid dtype is provide for the rand operation. use float32 and float64"
        )
    if generator is None:
        generator = C.GeneratorBase(random.randint(0, 100))
    return _use_utils_ops(
        shape=shape,
        generator=generator,
        requires_grad=requires_grad,
        operation_name="rand",
        dtype=dtype,
    )


def randint(*shape, low=0, high, generator=None, requires_grad=False, dtype=Th.int32):
    if dtype not in {Th.int32, Th.int64}:
        raise TypeError(
            "Invalid dtype is provide for the randint operation. use int32 and int64"
        )
    if generator is None:
        generator = C.GeneratorBase(random.randint(0, 100))
    return _use_utils_ops(
        shape=shape,
        low=low,
        high=high,
        generator=generator,
        requires_grad=requires_grad,
        operation_name="randint",
        dtype=dtype,
    )


rand.__module__ = "anygrad"
randint.__module__ = "anygrad"
