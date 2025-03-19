from typing import Optional, List, Tuple, Union

from anygrad.tensor.base import ThHelper as Th
from anygrad.tensor.base.ThHelper import float32
from anygrad.tensor.base.booltensor import BoolTensor
from anygrad.tensor.base.inttensor import IntTensor
from anygrad.tensor.base.floattensor import FloatTensor

from anygrad.version import __version__
from numpy import array


class Tensor:
    """
    Class to repesent a Tensor.

    Attributes
    ----------
    data : List | Tuple
        Any Iterable

    requires_grad: Optional[bool] = False
        if `True` the gradient caculation is happend

    dtype: Optional[anygrad.float32 | anygrad.float64 | anygrad.int32 | anygrad.int64 | anygrad.bool] = anygrad.float32

    Methods
    ----------
    data:
        return the item of the tensor in list form.
    shape:
        return the shape of the tensor in tuple form.
    ndim:
        return the dim of the tensor in int form.
    requires_grad:
        return the bool value if the requires_grad.
    grad:
        a tensor value that allow you to see the gredient of the tensor.

    add(other):
        other: Tensor | int | float
        add the Tensor or number.

    sub(other):
        other: Tensor | int | float
        sub the Tensor or number.

    mul(other):
        other: Tensor | int | float
        mul the Tensor or number.

    div(other):
        other: Tensor | int | float
        div the Tensor or number.

    pow(other):
        other: Tensor | int | float
        pow the Tensor or number.

    matmul(other):
        other: Tensor
        matrix multiplication of the Two valid shape tensor.

    sum(self, axis: Optional[int] = -1, keepdims: Optional[bool] = False) -> Tensor:
        sum the tensor with axis and keepdims.

    backward(self, custom_grad:Optional[Tensor] = None) -> None:
        Do the backward pass if the requires-grad is true for given tensor.

    """

    def __init__(
        self,
        data: List[int | float] | Tuple[int | float],
        requires_grad: Optional[bool] = False,
        dtype:any = float32,
    ) -> None:

        # requires_grad type checking
        if not isinstance(requires_grad, bool):
            raise TypeError(
                f"requires_grad is must be in bool not in {type(requires_grad)}"
            )

        if isinstance(data, (int, float)):
            data = [data]

        if isinstance(dtype, str):
            dtype = getattr(Th, dtype)
        valid_types = {Th.float32, Th.float64, Th.int32, Th.int64, Th.bool}
        if dtype not in valid_types:
            raise TypeError(
                "Tensor must have a valid dtype: 'float32', 'float64', 'int32', 'int64' or 'bool'."
            )

        if dtype not in {Th.float32, Th.float64} and requires_grad:
            raise RuntimeError(
                f"The requires_grad is only support for 'float32' and 'float64' for version {__version__}"
            )

        type_list = Th.valid_data_type(data)
        if dtype == Th.bool:
            self._tensor = BoolTensor(data, dtype=Th.bool)
        elif dtype in {Th.float32, Th.float64}:
            self._tensor = FloatTensor(data, requires_grad=requires_grad, dtype=dtype)
        elif dtype in {Th.int32, Th.int64}:
            self._tensor = IntTensor(data, dtype=dtype)
        else:
            raise TypeError(
                f"Given Datatype {type_list} is not support in current version {__version__}"
            )

    @property
    def shape(self) -> Tuple[int, ...]:
        return self._tensor.shape

    @property
    def ndim(self) -> int:
        return self._tensor.ndim

    @property
    def size(self) -> int:
        return self._tensor.size

    @property
    def dtype(self) -> str:
        return self._tensor.dtype

    @property
    def data(self):
        return self._tensor.data

    @property
    def base(self):
        return self._tensor.base

    @property
    def requires_grad(self):
        return self._tensor.requires_grad

    @requires_grad.setter
    def requires_grad(self, value):
        self._tensor.requires_grad = value

    @property
    def grad(self):
        return self._tensor.grad

    @grad.setter
    def grad(self, value):
        self._tensor.grad = value

    @property
    def _backward(self):
        return self._tensor._backward

    @_backward.setter
    def _backward(self, value):
        self._tensor._backward = value

    @property
    def _prev(self):
        return self._tensor._prev

    @_prev.setter
    def _prev(self, value):
        self._tensor._prev = value

    @property
    def is_leaf(self):
        return self._tensor.is_leaf

    @is_leaf.setter
    def is_leaf(self, value):
        self._tensor.is_leaf = value

    def __repr__(self) -> str:
        return repr(self._tensor)

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, index: Union[int, slice]) -> "Tensor":
        return self._tensor.__getitem__(index)

    def __add__(self, other: Union["Tensor", int, float]) -> "Tensor":
        return self._tensor.__add__(other)

    def __sub__(self, other: Union["Tensor", int, float]) -> "Tensor":
        return self._tensor.__sub__(other)

    def __mul__(self, other: Union["Tensor", int, float]) -> "Tensor":
        return self._tensor.__mul__(other)

    def __truediv__(self, other: Union["Tensor", int, float]) -> "Tensor":
        return self._tensor.__truediv__(other)

    def __matmul__(self, other: Union["Tensor", int, float]) -> "Tensor":
        return self._tensor.__matmul__(other)

    def __neg__(self) -> "Tensor":
        return self._tensor.__neg__()

    def __pow__(self, other: Union["Tensor", int, float]) -> "Tensor":
        return self._tensor.__pow__(other)

    def __radd__(self, other: Union["Tensor", int, float]) -> "Tensor":
        return self._tensor.__radd__(other)

    def __rsub__(self, other: Union["Tensor", int, float]) -> "Tensor":
        return self._tensor.__rsub__(other)

    def __rmul__(self, other: Union["Tensor", int, float]) -> "Tensor":
        return self._tensor.__rmul__(other)

    def __rtruediv__(self, other: Union["Tensor", int, float]) -> "Tensor":
        return self._tensor.__rtruediv__(other)
    
    def __eq__(self, other:Union["Tensor", int, float]) -> "Tensor":
        return self._tensor.__eq__(other)
    
    def __gt__(self, other:Union["Tensor", int, float]) -> "Tensor":
        return self._tensor.__gt__(other)
    
    def __lt__(self, other:Union["Tensor", int, float]) -> "Tensor":
        return self._tensor.__lt__(other)
    
    def __ge__(self, other:Union["Tensor", int, float]) -> "Tensor":
        return self._tensor.__ge__(other)
    
    def __le__(self, other:Union["Tensor", int, float]) -> "Tensor":
        return self._tensor.__le__(other)

    def sum(
        self, axis: Optional[int] = -1, keepdims: Optional[bool] = False
    ) -> "Tensor":
        return self._tensor.sum(axis=axis, keepdims=keepdims)

    def mean(
        self, axis: Optional[int] = -1, keepdims: Optional[bool] = False
    ) -> "Tensor":
        return self._tensor.mean(axis=axis, keepdims=keepdims)

    def min(
        self, axis: Optional[int] = -1, keepdims: Optional[bool] = False
    ) -> "Tensor":
        return self._tensor.min(axis=axis, keepdims=keepdims)

    def max(
        self, axis: Optional[int] = -1, keepdims: Optional[bool] = False
    ) -> "Tensor":
        return self._tensor.max(axis=axis, keepdims=keepdims)

    def median(
        self, axis: Optional[int] = -1, keepdims: Optional[bool] = False
    ) -> "Tensor":
        return self._tensor.median(axis=axis, keepdims=keepdims)

    def backward(self, custom_grad: Optional["Tensor"] = None) -> None:
        return self._tensor.backward(custom_grad)

    def transpose(self, dim0: int, dim1: int) -> "Tensor":
        return self._tensor.transpose(dim0, dim1)

    def zero_(self) -> "Tensor": return self._tensor.zero_()
    
    def view(self, *shape) -> "Tensor": return self._tensor.view(shape)
    
    def reshape(self, *shape) -> "Tensor":
        new_data = Th.reshape(self.data, shape)
        return Tensor(new_data, self.requires_grad, self.dtype)

    def __hash__(self):
        return id(self)
    
    def tolist(self):
        return self._tensor.data
    
    def tonumpy(self):
        return array(self._tensor.data)
    
    __module__ = "anygrad"
