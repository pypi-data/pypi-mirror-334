from typing import Optional, Tuple, Callable, Any

from anygrad.tensor.base import tensor_c as C
from anygrad.tensor.base import ThHelper as Th

import anygrad
import anygrad.autograd as Ag


class BaseTensor:

    _dtype_map = {
        "float32": Th.float32,
        "float64": Th.float64,
        "int32": Th.int32,
        "int64": Th.int64,
        "bool": Th.bool,
    }

    promotion_table = {
        (Th.bool, Th.bool) : Th.bool,
        
        (Th.int32, Th.int32): Th.int32,
        (Th.int32, Th.int64):Th.int64,
        (Th.int32, Th.float32):Th.float32,
        (Th.int32, Th.float64):Th.float64,
        
        (Th.int64, Th.int64): Th.int64,
        (Th.int64, Th.float32):Th.float32,
        (Th.int64, Th.float64):Th.float64,
        
        (Th.float32, Th.float32):Th.float32,
        (Th.float32, Th.float64):Th.float64,
        
        (Th.float64, Th.float64):Th.float64
    }
    
    @classmethod
    def promote_type(cls, type1, type2):
        return cls.promotion_table.get((type1, type2)) or cls.promotion_table.get((type2, type1))

    def __init__(self, requires_grad=False):

        self.requires_grad = requires_grad and Ag.GradMode.is_enabled()
        self.grad = None
        self.name_backward = ""
        self._backward = lambda: None
        self._prev = set()
        self.is_leaf = True

    @property
    def shape(self) -> Tuple[int, ...]:
        return tuple(self.base.shape)

    @property
    def ndim(self) -> int:
        return self.base.ndim

    @property
    def size(self) -> int:
        return self.base.size

    @property
    def dtype(self) -> str:
        return BaseTensor._dtype_map[self.base.dtype]
    
    @staticmethod
    def _create_tensor(ResultClass, OtherClass, allow_other_class, data, shape, dtype, req_grad):
        reshape = Th.reshape(data, shape)
        
        if allow_other_class:
            ans = OtherClass(reshape, requires_grad=req_grad, dtype=dtype)
        elif dtype in {Th.float32, Th.float64}:
            ans = OtherClass(reshape, requires_grad=req_grad, dtype=dtype)
        elif dtype in {Th.int32, Th.int64, Th.bool}:
            ans = ResultClass(reshape, dtype=dtype)
        return ans

    @staticmethod
    def _apply_operation(tensor1, 
                         tensor2, 
                         ResultClass, 
                         OtherClass, 
                         has_scaler:bool, 
                         operation:Callable, 
                         operation_name:str,
                         allow_other_class:bool, 
                         broadcast_check:Callable = C.isbroadcast):
        
        if isinstance(tensor2, (int, float)) and has_scaler:
            data = [operation(i, tensor2) for i in tensor1.base.data]
            ans = BaseTensor._create_tensor(ResultClass, OtherClass, allow_other_class, data, tensor1.base.shape, tensor1.dtype, tensor1.requires_grad)
            
            if ans.requires_grad:
                ans._prev = {tensor1}
                ans._backward = getattr(Ag.GradientCal, f"{operation_name.capitalize()}_grad")(tensor1, tensor2, ans)
                ans.name_backward = f"<{operation_name}Backward1>"
                ans.is_leaf = False
            return ans
        
        allow = broadcast_check(tensor1.base.shape, tensor2.base.shape, tensor1.base.ndim, tensor2.base.ndim)
        if not allow:
            raise RuntimeError(f"The size of the tensors are must broadcast current shapes are :{tensor1.base.shape} and {tensor2.base.shape}")
        
        func = getattr(C, f"{operation_name.capitalize()}", None)
        if func is None:
            raise NotImplementedError(f"""
                                      {operation_name} is not implemented in C++
                                      """)
        
        data, shape = func(tensor1.base, tensor2.base)
        dtype = BaseTensor.promote_type(tensor1.dtype, tensor2.dtype)
        req_grad = tensor1.requires_grad or tensor2.requires_grad
        ans = BaseTensor._create_tensor(ResultClass, OtherClass, allow_other_class, data, shape, dtype, req_grad)
        if ans.requires_grad:
            ans._prev = {tensor1, tensor2}
            ans._backward = getattr(Ag.GradientCal, f"{operation_name.capitalize()}_grad")(tensor1, tensor2, ans)
            ans.name_backward = f"<{operation_name}Bacward0>"
            ans.is_leaf = False
            
        return ans

    @staticmethod
    def _reduce_ops(tensor1, ResultClass, OtherClass, axis: Optional[int], keepdims: bool, operation_name: str, allow_other_class: bool = False):
        allow = C.is_sum_allow(axis, tensor1.base.ndim)
        if not allow:
            raise RuntimeError(f"Invalid reduction operation: axis {axis} is not compatible with tensor of dimension {tensor1.base.ndim}")

        func = getattr(C, f"{operation_name.capitalize()}", None)
        if func is None:
            raise NotImplementedError(f"{operation_name} is not implemented in C++")

        data, shape = func(tensor1.base, axis, keepdims)
        ans = BaseTensor._create_tensor(ResultClass, OtherClass, allow_other_class, 
                                      data, shape, tensor1.dtype, tensor1.requires_grad)

        if ans.requires_grad:
            ans._prev = {tensor1}
            ans._backward = getattr(Ag.GradientCal, f"{operation_name.capitalize()}_grad")(
                tensor1, ans
            )
            ans.name_backward = f"<{operation_name}Backward0>"
            ans.is_leaf = False

        return ans

    @staticmethod
    def _trans_ops(tensor1, ResultClass, OtherClass, dim0: int, dim1: int, allow_other_class: bool = False):
        if dim0 < 0 and dim1 < 0:
            dim0 = tensor1.ndim + dim0
            dim1 = tensor1.ndim + dim1

        if tensor1.ndim < 2:
            raise RuntimeError(f"Transpose requires at least 2D tensor, got {tensor1.ndim}D")
        
        func = getattr(C, f"Trans", None)
        if func is None:
            raise NotImplementedError("Transpose is not implemented in C++")
            
        data, shape = func(tensor1.base, dim0, dim1)
        ans = BaseTensor._create_tensor(ResultClass, OtherClass, allow_other_class,
                                      data, shape, tensor1.dtype, tensor1.requires_grad)

        if ans.requires_grad:
            ans._prev = {tensor1}
            ans.name_backward = "<TransBackward0>"
            ans._backward = getattr(Ag.GradientCal, "Trans_grad")(tensor1, ans)
            ans.is_leaf = False

        return ans
    
    @staticmethod
    def _apply_view(tensor1, ResultClass, OtherClass, shape, allow_other_class: bool = False):
        allow = C.is_view_allow(tensor1.base.shape, tensor1.base.size)
        if not allow:
            raise RuntimeError(f"Invalid view operation: shape {shape} is not compatible with tensor of size {tensor1.base.size}")
        
        func = getattr(C, f"View", None)
        if func is None:
            raise NotImplementedError("View is not implemented in C++")
        
        data, shape = func(tensor1.base, shape)
        ans = BaseTensor._create_tensor(ResultClass, OtherClass, allow_other_class,
                                      data, shape, tensor1.dtype, tensor1.requires_grad)
        
        if ans.requires_grad:
            ans._prev = {tensor1}
            ans.name_backward = "<ViewBackward0>"
            ans._backward = getattr(Ag.GradientCal, "View_grad")(tensor1, ans)
            ans.is_leaf = False
            
        return ans

    @staticmethod
    def _apply_reshape(tensor, shape, TensorClass):
        ans = BaseTensor._create_tensor(TensorClass, TensorClass, False,
                                      tensor.data, shape, tensor.dtype, tensor.requires_grad)
        
        if ans.requires_grad:
            ans._prev = {tensor}
            ans.name_backward = "<ReshapeBackward0>"
            ans._backward = getattr(Ag.GradientCal, "Reshape_grad")(tensor, ans)
            ans.is_leaf = False
        
        return ans
    
    @staticmethod
    def _apply_compare(tensor1, tensor2, ResultClass, operation, operation_name:str, has_scaler:bool, broadcast_check = C.isbroadcast):
        
        if isinstance(tensor2, (int, float)) and has_scaler:
            data, shape = [operation(tensor1.data[i], tensor2) for i in range(tensor1.size)]
            reshape = Th.reshape(data, shape)
            ans = ResultClass(reshape, dtype=Th.bool)
            return ans
        
        allow = broadcast_check(tensor1.base.shape, tensor2.base.shape, tensor1.base.ndim, tensor2.base.ndim)
        if not allow:
            raise RuntimeError(f"The size of the tensors are must broadcast current shapes are :{tensor1.base.shape} and {tensor2.base.shape}")
        
        func = getattr(C, f"{operation_name.capitalize()}", None)
        if func is None:
            raise NotImplementedError(f"""
                                      {operation_name} is not implemented in C++
                                      """)
        
        data, shape = func(tensor1.base, tensor2.base)
        reshape = Th.reshape(data, shape)
        ans = ResultClass(reshape, dtype=Th.bool)
        return ans
        
        
        
        
    def __iter__(self):
        return iter(self.data)

    def __neg__(self):
        return -1 * self

    def backward(self, custom_grad=None) -> None:
        if not self.requires_grad:
            raise ValueError("Backward pass only works if requires_grad is True")

        if self.shape == (1,):
            if custom_grad is not None:
                raise ValueError(
                    "Do not provide a custom gradient for scalar outputs; use a scalar value for grad computation"
                )
            self.grad = anygrad.ones_like(self, requires_grad=False, dtype=self.dtype)
        else:
            if custom_grad is None:
                raise ValueError(
                    "A custom gradient must be provided for non-scalar outputs"
                )
            if custom_grad.shape != self.shape:
                raise ValueError(
                    f"Custom grad shape {custom_grad.shape} doesn't match output shape {self.shape}"
                )
            self.grad = custom_grad

        topo = Ag.BuildGraph.construct_graph(self)

        for v in reversed(topo):
            if v is not self and v._prev:
                v.grad = None

        for v in topo:
            v._backward()
