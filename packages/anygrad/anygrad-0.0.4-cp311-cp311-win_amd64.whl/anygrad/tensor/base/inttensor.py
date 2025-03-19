from typing import Optional, List, Union
import pprint

from anygrad.tensor.base import tensor_c as C
from anygrad.tensor.base import ThHelper as Th
from anygrad.tensor.base.basetensor import BaseTensor
from anygrad.tensor.base.floattensor import FloatTensor
from anygrad.tensor.base.booltensor import BoolTensor


class IntTensor(BaseTensor):
    """
    Class to repesent a IntTensor.

    Attributes
    ----------
    data : List | Tuple
        Any Iterable

    dtype: Optional[anygrad.int32 | anygrad.int64] = anygrad.int32

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
        self, data: List[int], dtype: Optional[Th.int32 | Th.int64] = Th.int32
    ):
        super().__init__()

        if isinstance(data, (int, float)):
            data = [data]

        self.data = Th.convert_tensor(data, int)
        list_data = Th.flat_list(self.data)

        if isinstance(dtype, str):
            dtype = getattr(Th, dtype)

        shape = Th.cal_shape(data)

        if dtype == Th.int32:
            self.base = C.int32(list_data, shape)
        elif dtype == Th.int64:
            self.base = C.int64(list_data, shape)

    def __repr__(self) -> str:
        data = Th.round_list(self.data)
        format_data = pprint.pformat(data, width=150, depth=50)
        base_str = f"Tensor({format_data}"
        return base_str + f", dtype={self.dtype})"

    def __getitem__(self, index: Union[int, slice]) -> "IntTensor":
        new_data = self.data[index]
        return IntTensor(new_data, dtype=self.dtype)

    def __add__(self, other) -> "IntTensor":
        return BaseTensor._apply_operation(
            tensor1=self,
            tensor2=other,
            ResultClass=IntTensor,
            OtherClass=FloatTensor,
            has_scaler=True,
            operation=lambda x, y: x + y,
            operation_name="Add",
            allow_other_class=False
        )

    def __radd__(self, other) -> "IntTensor":
        return self._add__(other)

    def __sub__(self, other) -> "IntTensor":
        return BaseTensor._apply_operation(
            tensor1=self,
            tensor2=other,
            ResultClass=IntTensor,
            OtherClass=FloatTensor,
            has_scaler=True,
            operation=lambda x, y: x - y,
            operation_name="Sub",
            allow_other_class=False
        )

    def __rsub__(self, other) -> "IntTensor":
        return BaseTensor._apply_operation(
            tensor1=self,
            tensor2=other,
            ResultClass=IntTensor,
            OtherClass=FloatTensor,
            has_scaler=True,
            operation=lambda x, y: y + x,
            operation_name="Sub",
            allow_other_class=False
        )

    def __mul__(self, other) -> "IntTensor":
        return BaseTensor._apply_operation(
            tensor1=self,
            tensor2=other,
            ResultClass=IntTensor,
            OtherClass=FloatTensor,
            has_scaler=True,
            operation=lambda x, y: x * y,
            operation_name="Mul",
            allow_other_class=False
        )

    def __rmul__(self, other) -> "IntTensor":
        return self.__mul__(other)

    def __truediv__(self, other) -> "IntTensor":
        return BaseTensor._apply_operation(
            tensor1=self,
            tensor2=other,
            ResultClass=IntTensor,
            OtherClass=FloatTensor,
            has_scaler=True,
            operation=lambda x, y: x / y,
            operation_name="Div",
            allow_other_class=True
        )

    def __rtruediv__(self, other) -> "IntTensor":
        return BaseTensor._apply_operation(
            tensor1=self,
            tensor2=other,
            ResultClass=IntTensor,
            OtherClass=FloatTensor,
            has_scaler=True,
            operation=lambda x, y: y / x,
            operation_name="Div",
            allow_other_class=True
        )

    def __pow__(self, other) -> "IntTensor":
        return BaseTensor._apply_operation(
            tensor1=self,
            tensor2=other,
            ResultClass=IntTensor,
            OtherClass=FloatTensor,
            has_scaler=True,
            operation=lambda x, y: x ** y,
            operation_name="Pow",
            allow_other_class=False
        )

    def __matmul__(self, other) -> "IntTensor":
        return BaseTensor._apply_operation(
            tensor1=self,
            tensor2=other,
            ResultClass=IntTensor,
            OtherClass=FloatTensor,
            has_scaler=False,
            operation=None,
            operation_name="Matmul",
            allow_other_class=False,
            broadcast_check=C.is_matmul_broadcast
        )
        
    def __eq__(self, other):
        return BaseTensor._apply_compare(
            self,
            other,
            BoolTensor,
            operation = lambda x, y: x == y,
            operation_name = "Eq",
            has_scaler=True
        )
    
    def __gt__(self, other):
        return BaseTensor._apply_compare(
            self,
            other,
            BoolTensor,
            operation = lambda x, y: x > y,
            operation_name = "Gt",
            has_scaler=True
        )
        
    def __lt__(self, other):
        return BaseTensor._apply_compare(
            self,
            other,
            BoolTensor,
            operation = lambda x, y: x < y,
            operation_name = "Lt",
            has_scaler=True
        )
    
    def __ge__(self, other):
        return BaseTensor._apply_compare(
            self,
            other,
            BoolTensor,
            operation = lambda x, y: x >= y,
            operation_name = "Ge",
            has_scaler=True
        )
    
    def __le__(self, other):
        return BaseTensor._apply_compare(
            self,
            other,
            BoolTensor,
            operation = lambda x, y: x <= y,
            operation_name = "Le",
            has_scaler=True
        )

    def sum(self, axis: Optional[int] = -1, keepdims: Optional[bool] = False):
        return BaseTensor._reduce_ops(self, IntTensor, IntTensor, axis, keepdims, "Sum", allow_other_class=False)

    def mean(self, axis: Optional[int] = -1, keepdims: Optional[bool] = False):
        return BaseTensor._reduce_ops(self, IntTensor, FloatTensor, axis, keepdims, "Mean", allow_other_class=True)

    def min(self, axis: Optional[int] = -1, keepdims: Optional[bool] = False):
        return BaseTensor._reduce_ops(self, IntTensor, IntTensor, axis, keepdims, "Min", allow_other_class=False)

    def max(self, axis: Optional[int] = -1, keepdims: Optional[bool] = False):
        return BaseTensor._reduce_ops(self, IntTensor, IntTensor, axis, keepdims, "Max", allow_other_class=False)

    def median(self, axis: Optional[int] = -1, keepdims: Optional[bool] = False):
        return BaseTensor._reduce_ops(self, IntTensor, FloatTensor, axis, keepdims, "Median", allow_other_class=True)

    def transpose(self, dim0: int, dim1: int) -> "IntTensor":
        return BaseTensor._trans_ops(self, IntTensor, FloatTensor, dim0, dim1, allow_other_class=False)

    def zero_(self) -> "IntTensor":
        """Zeros out the tensor in-place."""
        self.data = [[0] * dim for dim in self.shape]
        self.base = C.int32(Th.flat_list(self.data), self.shape) if self.dtype == "int32" else C.int64(Th.flat_list(self.data), self.shape)
        return self

    def view(self, shape) -> "IntTensor":
        return BaseTensor._apply_view(self, IntTensor, FloatTensor, shape, allow_other_class=False)

    __module__ = "anygrad"
