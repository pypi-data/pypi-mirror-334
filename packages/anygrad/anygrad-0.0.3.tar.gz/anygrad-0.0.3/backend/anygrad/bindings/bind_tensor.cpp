#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "../include/Th.hpp"

#include <vector>
#include <variant>
using namespace std;

namespace py = pybind11;

#define REGISTER_OPS(name, T1, T2) msg.def(#name, [](const T1 &tensor1, const T2 &tensor2){ return name(tensor1, tensor2); })
#define REGISTER_REDUCE_OPS(name, T1) msg.def(#name, [](const T1 &tensor, int32_t dim, bool keepdims) { return name(tensor, dim, keepdims); })
#define REGISTER_TRANS_OPS(name, T1) msg.def(#name, [](const T1 &tensor, int32_t dim0, int32_t dim1) {return name(tensor, dim0, dim1);})
#define REGISTER_VIEW_OPS(name, T1) msg.def(#name, [](const T1 &tensor, vector_i16 rearrenge_view) {return name(tensor, rearrenge_view);})

PYBIND11_MODULE(tensor_c, msg) {
    py::class_<FloatTensorBase>(msg, "float32")
        .def(py::init<vector<float>, vector<int16_t>>())
        .def_readonly("data", &FloatTensorBase::data)
        .def_readonly("shape", &FloatTensorBase::shape)
        .def_readonly("ndim", &FloatTensorBase::ndim)
        .def_readonly("dtype", &FloatTensorBase::dtype)
        .def_readonly("size", &FloatTensorBase::size)
        ;
        
    py::class_<DoubleTensorBase>(msg, "float64")
        .def(py::init<vector<double>, vector<int16_t>>())
        .def_readonly("data", &DoubleTensorBase::data)
        .def_readonly("shape", &DoubleTensorBase::shape)
        .def_readonly("ndim", &DoubleTensorBase::ndim)
        .def_readonly("dtype", &DoubleTensorBase::dtype)
        .def_readonly("size", &DoubleTensorBase::size)
        ;

    py::class_<Int32TensorBase>(msg, "int32")
        .def(py::init<vector<int32_t>, vector<int16_t>>())
        .def_readonly("data", &Int32TensorBase::data)
        .def_readonly("shape", &Int32TensorBase::shape)
        .def_readonly("ndim", &Int32TensorBase::ndim)
        .def_readonly("dtype", &Int32TensorBase::dtype)
        .def_readonly("size", &Int32TensorBase::size)
        ;

    py::class_<Int64TensorBase>(msg, "int64")
        .def(py::init<vector<int64_t>, vector<int16_t>>())
        .def_readonly("data", &Int64TensorBase::data)
        .def_readonly("shape", &Int64TensorBase::shape)
        .def_readonly("ndim", &Int64TensorBase::ndim)
        .def_readonly("dtype", &Int64TensorBase::dtype)
        .def_readonly("size", &Int64TensorBase::size)
        ;

    py::class_<BoolTensorBase>(msg, "bool")
        .def(py::init<vector<bool>, vector<int16_t>>())
        .def_readonly("data", &BoolTensorBase::data)
        .def_readonly("shape", &BoolTensorBase::shape)
        .def_readonly("ndim", &BoolTensorBase::ndim)
        .def_readonly("dtype", &BoolTensorBase::dtype)
        .def_readonly("size", &BoolTensorBase::size)
        ;
    
    //arithmetic

    REGISTER_OPS(Add, FloatTensorBase, FloatTensorBase);
    REGISTER_OPS(Add, FloatTensorBase, DoubleTensorBase);
    REGISTER_OPS(Add, DoubleTensorBase, FloatTensorBase);
    REGISTER_OPS(Add, FloatTensorBase, Int32TensorBase);
    REGISTER_OPS(Add, Int32TensorBase, FloatTensorBase);
    REGISTER_OPS(Add, FloatTensorBase, Int64TensorBase);
    REGISTER_OPS(Add, Int64TensorBase, FloatTensorBase);
    REGISTER_OPS(Add, DoubleTensorBase, DoubleTensorBase);
    REGISTER_OPS(Add, DoubleTensorBase, Int32TensorBase);
    REGISTER_OPS(Add, Int32TensorBase, DoubleTensorBase);
    REGISTER_OPS(Add, DoubleTensorBase, Int64TensorBase);
    REGISTER_OPS(Add, Int64TensorBase, DoubleTensorBase);
    REGISTER_OPS(Add, Int32TensorBase, Int32TensorBase);
    REGISTER_OPS(Add, Int32TensorBase, Int64TensorBase);
    REGISTER_OPS(Add, Int64TensorBase, Int64TensorBase);
    REGISTER_OPS(Add, BoolTensorBase, BoolTensorBase);

    REGISTER_OPS(Sub, FloatTensorBase, FloatTensorBase);
    REGISTER_OPS(Sub, FloatTensorBase, DoubleTensorBase);
    REGISTER_OPS(Sub, DoubleTensorBase, FloatTensorBase);
    REGISTER_OPS(Sub, FloatTensorBase, Int32TensorBase);
    REGISTER_OPS(Sub, Int32TensorBase, FloatTensorBase);
    REGISTER_OPS(Sub, FloatTensorBase, Int64TensorBase);
    REGISTER_OPS(Sub, Int64TensorBase, FloatTensorBase);
    REGISTER_OPS(Sub, DoubleTensorBase, DoubleTensorBase);
    REGISTER_OPS(Sub, DoubleTensorBase, Int32TensorBase);
    REGISTER_OPS(Sub, Int32TensorBase, DoubleTensorBase);
    REGISTER_OPS(Sub, DoubleTensorBase, Int64TensorBase);
    REGISTER_OPS(Sub, Int64TensorBase, DoubleTensorBase);
    REGISTER_OPS(Sub, Int32TensorBase, Int32TensorBase);
    REGISTER_OPS(Sub, Int32TensorBase, Int64TensorBase);
    REGISTER_OPS(Sub, Int64TensorBase, Int64TensorBase);
    REGISTER_OPS(Sub, BoolTensorBase, BoolTensorBase);

    REGISTER_OPS(Mul, FloatTensorBase, FloatTensorBase);
    REGISTER_OPS(Mul, FloatTensorBase, DoubleTensorBase);
    REGISTER_OPS(Mul, DoubleTensorBase, FloatTensorBase);
    REGISTER_OPS(Mul, FloatTensorBase, Int32TensorBase);
    REGISTER_OPS(Mul, Int32TensorBase, FloatTensorBase);
    REGISTER_OPS(Mul, FloatTensorBase, Int64TensorBase);
    REGISTER_OPS(Mul, Int64TensorBase, FloatTensorBase);
    REGISTER_OPS(Mul, DoubleTensorBase, DoubleTensorBase);
    REGISTER_OPS(Mul, DoubleTensorBase, Int32TensorBase);
    REGISTER_OPS(Mul, Int32TensorBase, DoubleTensorBase);
    REGISTER_OPS(Mul, DoubleTensorBase, Int64TensorBase);
    REGISTER_OPS(Mul, Int64TensorBase, DoubleTensorBase);
    REGISTER_OPS(Mul, Int32TensorBase, Int32TensorBase);
    REGISTER_OPS(Mul, Int32TensorBase, Int64TensorBase);
    REGISTER_OPS(Mul, Int64TensorBase, Int64TensorBase);
    REGISTER_OPS(Mul, BoolTensorBase, BoolTensorBase);

    REGISTER_OPS(Div, FloatTensorBase, FloatTensorBase);
    REGISTER_OPS(Div, FloatTensorBase, DoubleTensorBase);
    REGISTER_OPS(Div, DoubleTensorBase, FloatTensorBase);
    REGISTER_OPS(Div, FloatTensorBase, Int32TensorBase);
    REGISTER_OPS(Div, Int32TensorBase, FloatTensorBase);
    REGISTER_OPS(Div, FloatTensorBase, Int64TensorBase);
    REGISTER_OPS(Div, Int64TensorBase, FloatTensorBase);
    REGISTER_OPS(Div, DoubleTensorBase, DoubleTensorBase);
    REGISTER_OPS(Div, DoubleTensorBase, Int32TensorBase);
    REGISTER_OPS(Div, Int32TensorBase, DoubleTensorBase);
    REGISTER_OPS(Div, DoubleTensorBase, Int64TensorBase);
    REGISTER_OPS(Div, Int64TensorBase, DoubleTensorBase);
    REGISTER_OPS(Div, Int32TensorBase, Int32TensorBase);
    REGISTER_OPS(Div, Int32TensorBase, Int64TensorBase);
    REGISTER_OPS(Div, Int64TensorBase, Int64TensorBase);
    REGISTER_OPS(Div, BoolTensorBase, BoolTensorBase);

    REGISTER_OPS(Pow, FloatTensorBase, FloatTensorBase);
    REGISTER_OPS(Pow, FloatTensorBase, DoubleTensorBase);
    REGISTER_OPS(Pow, DoubleTensorBase, FloatTensorBase);
    REGISTER_OPS(Pow, FloatTensorBase, Int32TensorBase);
    REGISTER_OPS(Pow, Int32TensorBase, FloatTensorBase);
    REGISTER_OPS(Pow, FloatTensorBase, Int64TensorBase);
    REGISTER_OPS(Pow, Int64TensorBase, FloatTensorBase);
    REGISTER_OPS(Pow, DoubleTensorBase, DoubleTensorBase);
    REGISTER_OPS(Pow, DoubleTensorBase, Int32TensorBase);
    REGISTER_OPS(Pow, Int32TensorBase, DoubleTensorBase);
    REGISTER_OPS(Pow, DoubleTensorBase, Int64TensorBase);
    REGISTER_OPS(Pow, Int64TensorBase, DoubleTensorBase);
    REGISTER_OPS(Pow, Int32TensorBase, Int32TensorBase);
    REGISTER_OPS(Pow, Int32TensorBase, Int64TensorBase);
    REGISTER_OPS(Pow, Int64TensorBase, Int64TensorBase);
    REGISTER_OPS(Pow, BoolTensorBase, BoolTensorBase);

    REGISTER_OPS(Eq, FloatTensorBase, FloatTensorBase);
    REGISTER_OPS(Eq, FloatTensorBase, DoubleTensorBase);
    REGISTER_OPS(Eq, DoubleTensorBase, FloatTensorBase);
    REGISTER_OPS(Eq, FloatTensorBase, Int32TensorBase);
    REGISTER_OPS(Eq, Int32TensorBase, FloatTensorBase);
    REGISTER_OPS(Eq, FloatTensorBase, Int64TensorBase);
    REGISTER_OPS(Eq, Int64TensorBase, FloatTensorBase);
    REGISTER_OPS(Eq, DoubleTensorBase, DoubleTensorBase);
    REGISTER_OPS(Eq, DoubleTensorBase, Int32TensorBase);
    REGISTER_OPS(Eq, Int32TensorBase, DoubleTensorBase);
    REGISTER_OPS(Eq, DoubleTensorBase, Int64TensorBase);
    REGISTER_OPS(Eq, Int64TensorBase, DoubleTensorBase);
    REGISTER_OPS(Eq, Int32TensorBase, Int32TensorBase);
    REGISTER_OPS(Eq, Int32TensorBase, Int64TensorBase);
    REGISTER_OPS(Eq, Int64TensorBase, Int64TensorBase);
    REGISTER_OPS(Eq, BoolTensorBase, BoolTensorBase);

    REGISTER_OPS(Gt, FloatTensorBase, FloatTensorBase);
    REGISTER_OPS(Gt, FloatTensorBase, DoubleTensorBase);
    REGISTER_OPS(Gt, DoubleTensorBase, FloatTensorBase);
    REGISTER_OPS(Gt, FloatTensorBase, Int32TensorBase);
    REGISTER_OPS(Gt, Int32TensorBase, FloatTensorBase);
    REGISTER_OPS(Gt, FloatTensorBase, Int64TensorBase);
    REGISTER_OPS(Gt, Int64TensorBase, FloatTensorBase);
    REGISTER_OPS(Gt, DoubleTensorBase, DoubleTensorBase);
    REGISTER_OPS(Gt, DoubleTensorBase, Int32TensorBase);
    REGISTER_OPS(Gt, Int32TensorBase, DoubleTensorBase);
    REGISTER_OPS(Gt, DoubleTensorBase, Int64TensorBase);
    REGISTER_OPS(Gt, Int64TensorBase, DoubleTensorBase);
    REGISTER_OPS(Gt, Int32TensorBase, Int32TensorBase);
    REGISTER_OPS(Gt, Int32TensorBase, Int64TensorBase);
    REGISTER_OPS(Gt, Int64TensorBase, Int64TensorBase);
    REGISTER_OPS(Gt, BoolTensorBase, BoolTensorBase);

    REGISTER_OPS(Lt, FloatTensorBase, FloatTensorBase);
    REGISTER_OPS(Lt, FloatTensorBase, DoubleTensorBase);
    REGISTER_OPS(Lt, DoubleTensorBase, FloatTensorBase);
    REGISTER_OPS(Lt, FloatTensorBase, Int32TensorBase);
    REGISTER_OPS(Lt, Int32TensorBase, FloatTensorBase);
    REGISTER_OPS(Lt, FloatTensorBase, Int64TensorBase);
    REGISTER_OPS(Lt, Int64TensorBase, FloatTensorBase);
    REGISTER_OPS(Lt, DoubleTensorBase, DoubleTensorBase);
    REGISTER_OPS(Lt, DoubleTensorBase, Int32TensorBase);
    REGISTER_OPS(Lt, Int32TensorBase, DoubleTensorBase);
    REGISTER_OPS(Lt, DoubleTensorBase, Int64TensorBase);
    REGISTER_OPS(Lt, Int64TensorBase, DoubleTensorBase);
    REGISTER_OPS(Lt, Int32TensorBase, Int32TensorBase);
    REGISTER_OPS(Lt, Int32TensorBase, Int64TensorBase);
    REGISTER_OPS(Lt, Int64TensorBase, Int64TensorBase);
    REGISTER_OPS(Lt, BoolTensorBase, BoolTensorBase);

    REGISTER_OPS(Ge, FloatTensorBase, FloatTensorBase);
    REGISTER_OPS(Ge, FloatTensorBase, DoubleTensorBase);
    REGISTER_OPS(Ge, DoubleTensorBase, FloatTensorBase);
    REGISTER_OPS(Ge, FloatTensorBase, Int32TensorBase);
    REGISTER_OPS(Ge, Int32TensorBase, FloatTensorBase);
    REGISTER_OPS(Ge, FloatTensorBase, Int64TensorBase);
    REGISTER_OPS(Ge, Int64TensorBase, FloatTensorBase);
    REGISTER_OPS(Ge, DoubleTensorBase, DoubleTensorBase);
    REGISTER_OPS(Ge, DoubleTensorBase, Int32TensorBase);
    REGISTER_OPS(Ge, Int32TensorBase, DoubleTensorBase);
    REGISTER_OPS(Ge, DoubleTensorBase, Int64TensorBase);
    REGISTER_OPS(Ge, Int64TensorBase, DoubleTensorBase);
    REGISTER_OPS(Ge, Int32TensorBase, Int32TensorBase);
    REGISTER_OPS(Ge, Int32TensorBase, Int64TensorBase);
    REGISTER_OPS(Ge, Int64TensorBase, Int64TensorBase);
    REGISTER_OPS(Ge, BoolTensorBase, BoolTensorBase);

    REGISTER_OPS(Le, FloatTensorBase, FloatTensorBase);
    REGISTER_OPS(Le, FloatTensorBase, DoubleTensorBase);
    REGISTER_OPS(Le, DoubleTensorBase, FloatTensorBase);
    REGISTER_OPS(Le, FloatTensorBase, Int32TensorBase);
    REGISTER_OPS(Le, Int32TensorBase, FloatTensorBase);
    REGISTER_OPS(Le, FloatTensorBase, Int64TensorBase);
    REGISTER_OPS(Le, Int64TensorBase, FloatTensorBase);
    REGISTER_OPS(Le, DoubleTensorBase, DoubleTensorBase);
    REGISTER_OPS(Le, DoubleTensorBase, Int32TensorBase);
    REGISTER_OPS(Le, Int32TensorBase, DoubleTensorBase);
    REGISTER_OPS(Le, DoubleTensorBase, Int64TensorBase);
    REGISTER_OPS(Le, Int64TensorBase, DoubleTensorBase);
    REGISTER_OPS(Le, Int32TensorBase, Int32TensorBase);
    REGISTER_OPS(Le, Int32TensorBase, Int64TensorBase);
    REGISTER_OPS(Le, Int64TensorBase, Int64TensorBase);
    REGISTER_OPS(Le, BoolTensorBase, BoolTensorBase);

    REGISTER_REDUCE_OPS(Sum, FloatTensorBase);
    REGISTER_REDUCE_OPS(Sum, DoubleTensorBase);
    REGISTER_REDUCE_OPS(Sum, Int32TensorBase);
    REGISTER_REDUCE_OPS(Sum, Int64TensorBase);

    REGISTER_REDUCE_OPS(Mean, FloatTensorBase);
    REGISTER_REDUCE_OPS(Mean, DoubleTensorBase);
    REGISTER_REDUCE_OPS(Mean, Int32TensorBase);
    REGISTER_REDUCE_OPS(Mean, Int64TensorBase);

    REGISTER_REDUCE_OPS(Median, FloatTensorBase);
    REGISTER_REDUCE_OPS(Median, DoubleTensorBase);
    REGISTER_REDUCE_OPS(Median, Int32TensorBase);
    REGISTER_REDUCE_OPS(Median, Int64TensorBase);

    REGISTER_REDUCE_OPS(Min, FloatTensorBase);
    REGISTER_REDUCE_OPS(Min, DoubleTensorBase);
    REGISTER_REDUCE_OPS(Min, Int32TensorBase);
    REGISTER_REDUCE_OPS(Min, Int64TensorBase);

    REGISTER_REDUCE_OPS(Max, FloatTensorBase);
    REGISTER_REDUCE_OPS(Max, DoubleTensorBase);
    REGISTER_REDUCE_OPS(Max, Int32TensorBase);
    REGISTER_REDUCE_OPS(Max, Int64TensorBase);

    //rules
    msg.def("isbroadcast", &isbroadcast);
    msg.def("is_sum_allow", &is_sum_allow);
    msg.def("is_view_allow", &is_view_allow);

    //gemm
    REGISTER_OPS(Matmul, FloatTensorBase, FloatTensorBase);
    REGISTER_OPS(Matmul, DoubleTensorBase, DoubleTensorBase);
    REGISTER_OPS(Matmul, Int32TensorBase, Int32TensorBase);
    REGISTER_OPS(Matmul, Int64TensorBase, Int64TensorBase);
    REGISTER_TRANS_OPS(Trans, FloatTensorBase);
    REGISTER_TRANS_OPS(Trans, DoubleTensorBase);
    REGISTER_TRANS_OPS(Trans, Int32TensorBase);
    REGISTER_TRANS_OPS(Trans, Int64TensorBase);
    REGISTER_TRANS_OPS(Trans, BoolTensorBase);
    msg.def("is_matmul_broadcast", &is_matmul_broadcast);
    
    // msg.def("DEBUG_64", &DEBUG_64);
    //view
    REGISTER_VIEW_OPS(View, FloatTensorBase);
    REGISTER_VIEW_OPS(View, DoubleTensorBase);
    REGISTER_VIEW_OPS(View, Int32TensorBase);
    REGISTER_VIEW_OPS(View, Int64TensorBase);
    REGISTER_VIEW_OPS(View, BoolTensorBase);
}
