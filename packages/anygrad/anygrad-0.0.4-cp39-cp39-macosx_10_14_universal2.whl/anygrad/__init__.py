"""
    AnyGrad (anygrad)
    ----------
    A Python module that use C++ for Tensor operations.

"""
from anygrad.tensor.tensor import Tensor
from anygrad.tensor.base.floattensor import FloatTensor
from anygrad.tensor.base.inttensor import IntTensor
from anygrad.tensor.base.booltensor import BoolTensor
from anygrad.tensor.base.ThHelper import float32, float64, int32, int64, bool
from anygrad.autograd import no_grad
from anygrad.utils import (Generator, rand, randint, ones, ones_like, zeros, zeros_like, 
                    log, exp, exp2, log10, log2)
from anygrad.version import __version__


def matmul(tensor1, tensor2):
    return tensor1 @ tensor2


def cast(tensor: Tensor, target_dtype):
    return Tensor(tensor.data, requires_grad=tensor.requires_grad, dtype=target_dtype)


__all__ = [
    "Tensor", "FloatTensor", "IntTensor", "BoolTensor", "float32", "float64", "int32", "int64", "bool", "no_grad", 
    "Generator", "rand", "randint", "ones", "ones_like", "zeros", "zeros_like", "log", "log2", "log10", "log2", "exp", "exp2", "matmul", "cast", 
    "__version__",
]
