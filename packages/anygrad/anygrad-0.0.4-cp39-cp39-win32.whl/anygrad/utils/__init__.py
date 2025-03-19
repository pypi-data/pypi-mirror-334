from anygrad.utils.generator import Generator, rand, randint
from anygrad.tensor.tensor import Tensor
from anygrad.tensor.base.basetensor import BaseTensor
from anygrad.tensor.base import ThHelper as Th
from anygrad.tensor.tensor import Tensor
from anygrad.utils import utils_c as C

from typing import Tuple, Optional
import anygrad

def _get_dtype_str(dtype):
    for key, val in BaseTensor._dtype_map.items():
        if val == dtype:
            return key.capitalize()

def _use_ops_zeros_ones(shape: tuple, requires_grad: bool, dtype: any, operation_name: str):
    try:
        operation_func = getattr(
            C,
            f"{operation_name.capitalize()}{_get_dtype_str(dtype)}"
        )
    except Exception as e:
        raise NotImplementedError(f"{operation_name} is not Imlemented for {dtype}.") from e

    data, shape = operation_func(shape)
    ans = Th.reshape(data, shape)
    ans = Tensor(ans, dtype=dtype, requires_grad=requires_grad)
    return ans


def _use_ops_log(tensor1, requires_grad: bool, operation_name: str):
    try:
        op_func = getattr(
            C, f"{operation_name.capitalize()}{tensor1.base.dtype.capitalize()}"
        )
    except Exception as e:
        raise NotImplementedError(f"{operation_name} is not Imlemented for {tensor1.base.dtype}.") from e

    data, shape = op_func(tensor1.base)
    ans = Th.reshape(data, shape)
    if tensor1.dtype == Th.int32:
        ans = Tensor(ans, dtype=Th.float32, requires_grad=requires_grad)
    elif tensor1.dtype == Th.int64:
        ans = Tensor(ans, dtype=Th.float64, requires_grad=requires_grad)
    else:
        ans = Tensor(ans, dtype=tensor1.base.dtype, requires_grad=requires_grad)
    return ans

def zeros(
    *shape: Tuple[int],
    requires_grad: Optional[bool] = False,
    dtype: Optional[anygrad.float32 | anygrad.float64] = anygrad.float32,
) -> Tensor:
    return _use_ops_zeros_ones(
        shape=shape, requires_grad=requires_grad, dtype=dtype, operation_name="Zeros"
    )


def ones(
    *shape: Tuple[int],
    requires_grad: Optional[bool] = False,
    dtype: Optional[anygrad.float32 | anygrad.float64] = anygrad.float32,
) -> Tensor:
    return _use_ops_zeros_ones(
        shape=shape, requires_grad=requires_grad, dtype=dtype, operation_name="Ones"
    )


def zeros_like(
    tensor: Tensor,
    requires_grad: Optional[bool] = False,
    dtype: Optional[anygrad.float32 | anygrad.float64] = anygrad.float32,
) -> Tensor:
    requires_grad = (
        requires_grad if requires_grad is not False else tensor.requires_grad
    )
    return zeros(*tensor.shape, requires_grad=requires_grad, dtype=dtype)


def ones_like(
    tensor: Tensor,
    requires_grad: Optional[bool] = False,
    dtype: Optional[anygrad.float32 | anygrad.float64] = anygrad.float32,
) -> Tensor:
    requires_grad = (
        requires_grad if requires_grad is not False else tensor.requires_grad
    )
    return ones(*tensor.shape, requires_grad=requires_grad, dtype=dtype)


def log(tensor: Tensor, requires_grad: Optional[bool] = False) -> Tensor:
    return _use_ops_log(tensor, requires_grad=requires_grad, operation_name="Log")


def log10(tensor: Tensor, requires_grad: Optional[bool] = False) -> Tensor:
    return _use_ops_log(tensor, requires_grad=requires_grad, operation_name="Log10")


def log2(tensor: Tensor, requires_grad: Optional[bool] = False) -> Tensor:
    return _use_ops_log(tensor, requires_grad=requires_grad, operation_name="Log2")


def exp(tensor: Tensor, requires_grad: Optional[bool] = False) -> Tensor:
    return _use_ops_log(tensor, requires_grad=requires_grad, operation_name="Exp")


def exp2(tensor: Tensor, requires_grad: Optional[bool] = False) -> Tensor:
    return _use_ops_log(tensor, requires_grad=requires_grad, operation_name="Exp2")


zeros.__module__ = "anygrad"
ones.__module__ = "anygrad"
ones_like.__module__ = "anygrad"
zeros_like.__module__ = "anygrad"
log.__module__ = "anygrad"
log10.__module__ = "anygrad"
log2.__module__ = "anygrad"
exp.__module__ = "anygrad"
exp2.__module__ = "anygrad"

__all__ = ["Generator", "rand", "randint"]
