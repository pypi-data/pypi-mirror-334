#ifndef THALLOPS_HPP
#define THALLOPS_HPP

#include <vector>
#include <utility>

#include "ThTypes.hpp"

using namespace std;

pair<vector_f32, vector_i16> Add(FloatTensorBase tensor1, FloatTensorBase tensor2);
pair<vector_f64, vector_i16> Add(DoubleTensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_i32, vector_i16> Add(Int32TensorBase tensor1, Int32TensorBase tensor2);
pair<vector_i64, vector_i16> Add(Int64TensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Add(BoolTensorBase tensor1, BoolTensorBase tensor2);
pair<vector_f64, vector_i16> Add(FloatTensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_i64, vector_i16> Add(Int32TensorBase tensor1, Int64TensorBase tensor2);
pair<vector_f32, vector_i16> Add(FloatTensorBase tensor1, Int32TensorBase tensor2);
pair<vector_f64, vector_i16> Add(DoubleTensorBase tensor1, Int32TensorBase tensor2);
pair<vector_f32, vector_i16> Add(FloatTensorBase tensor1, Int64TensorBase tensor2);
pair<vector_f64, vector_i16> Add(DoubleTensorBase tensor1, Int64TensorBase tensor2);
pair<vector_f64, vector_i16> Add(DoubleTensorBase tensor1, FloatTensorBase tensor2);
pair<vector_f32, vector_i16> Add(Int32TensorBase tensor1, FloatTensorBase tensor2);
pair<vector_f32, vector_i16> Add(Int64TensorBase tensor1, FloatTensorBase tensor2);
pair<vector_f64, vector_i16> Add(Int32TensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_f64, vector_i16> Add(Int64TensorBase tensor1, DoubleTensorBase tensor2);

pair<vector_f32, vector_i16> Sub(FloatTensorBase tensor1, FloatTensorBase tensor2);
pair<vector_f64, vector_i16> Sub(DoubleTensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_i32, vector_i16> Sub(Int32TensorBase tensor1, Int32TensorBase tensor2);
pair<vector_i64, vector_i16> Sub(Int64TensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Sub(BoolTensorBase tensor1, BoolTensorBase tensor2);
pair<vector_f64, vector_i16> Sub(FloatTensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_i64, vector_i16> Sub(Int32TensorBase tensor1, Int64TensorBase tensor2);
pair<vector_f32, vector_i16> Sub(FloatTensorBase tensor1, Int32TensorBase tensor2);
pair<vector_f64, vector_i16> Sub(DoubleTensorBase tensor1, Int32TensorBase tensor2);
pair<vector_f32, vector_i16> Sub(FloatTensorBase tensor1, Int64TensorBase tensor2);
pair<vector_f64, vector_i16> Sub(DoubleTensorBase tensor1, Int64TensorBase tensor2);
pair<vector_f64, vector_i16> Sub(DoubleTensorBase tensor1, FloatTensorBase tensor2);
pair<vector_f32, vector_i16> Sub(Int32TensorBase tensor1, FloatTensorBase tensor2);
pair<vector_f32, vector_i16> Sub(Int64TensorBase tensor1, FloatTensorBase tensor2);
pair<vector_f64, vector_i16> Sub(Int32TensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_f64, vector_i16> Sub(Int64TensorBase tensor1, DoubleTensorBase tensor2);

pair<vector_f32, vector_i16> Mul(FloatTensorBase tensor1, FloatTensorBase tensor2);
pair<vector_f64, vector_i16> Mul(DoubleTensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_i32, vector_i16> Mul(Int32TensorBase tensor1, Int32TensorBase tensor2);
pair<vector_i64, vector_i16> Mul(Int64TensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Mul(BoolTensorBase tensor1, BoolTensorBase tensor2);
pair<vector_f64, vector_i16> Mul(FloatTensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_i64, vector_i16> Mul(Int32TensorBase tensor1, Int64TensorBase tensor2);
pair<vector_f32, vector_i16> Mul(FloatTensorBase tensor1, Int32TensorBase tensor2);
pair<vector_f64, vector_i16> Mul(DoubleTensorBase tensor1, Int32TensorBase tensor2);
pair<vector_f32, vector_i16> Mul(FloatTensorBase tensor1, Int64TensorBase tensor2);
pair<vector_f64, vector_i16> Mul(DoubleTensorBase tensor1, Int64TensorBase tensor2);
pair<vector_f64, vector_i16> Mul(DoubleTensorBase tensor1, FloatTensorBase tensor2);
pair<vector_f32, vector_i16> Mul(Int32TensorBase tensor1, FloatTensorBase tensor2);
pair<vector_f32, vector_i16> Mul(Int64TensorBase tensor1, FloatTensorBase tensor2);
pair<vector_f64, vector_i16> Mul(Int32TensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_f64, vector_i16> Mul(Int64TensorBase tensor1, DoubleTensorBase tensor2);

pair<vector_f32, vector_i16> Div(FloatTensorBase tensor1, FloatTensorBase tensor2);
pair<vector_f64, vector_i16> Div(DoubleTensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_f32, vector_i16> Div(Int32TensorBase tensor1, Int32TensorBase tensor2);
pair<vector_f64, vector_i16> Div(Int64TensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Div(BoolTensorBase tensor1, BoolTensorBase tensor2);
pair<vector_f64, vector_i16> Div(FloatTensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_f64, vector_i16> Div(Int32TensorBase tensor1, Int64TensorBase tensor2);
pair<vector_f32, vector_i16> Div(FloatTensorBase tensor1, Int32TensorBase tensor2);
pair<vector_f64, vector_i16> Div(DoubleTensorBase tensor1, Int32TensorBase tensor2);
pair<vector_f32, vector_i16> Div(FloatTensorBase tensor1, Int64TensorBase tensor2);
pair<vector_f64, vector_i16> Div(DoubleTensorBase tensor1, Int64TensorBase tensor2);
pair<vector_f64, vector_i16> Div(DoubleTensorBase tensor1, FloatTensorBase tensor2);
pair<vector_f32, vector_i16> Div(Int32TensorBase tensor1, FloatTensorBase tensor2);
pair<vector_f32, vector_i16> Div(Int64TensorBase tensor1, FloatTensorBase tensor2);
pair<vector_f64, vector_i16> Div(Int32TensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_f64, vector_i16> Div(Int64TensorBase tensor1, DoubleTensorBase tensor2);

pair<vector_f32, vector_i16> Pow(FloatTensorBase tensor1, FloatTensorBase tensor2);
pair<vector_f64, vector_i16> Pow(DoubleTensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_i32, vector_i16> Pow(Int32TensorBase tensor1, Int32TensorBase tensor2);
pair<vector_i64, vector_i16> Pow(Int64TensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Pow(BoolTensorBase tensor1, BoolTensorBase tensor2);
pair<vector_f64, vector_i16> Pow(FloatTensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_i64, vector_i16> Pow(Int32TensorBase tensor1, Int64TensorBase tensor2);
pair<vector_f32, vector_i16> Pow(FloatTensorBase tensor1, Int32TensorBase tensor2);
pair<vector_f64, vector_i16> Pow(DoubleTensorBase tensor1, Int32TensorBase tensor2);
pair<vector_f32, vector_i16> Pow(FloatTensorBase tensor1, Int64TensorBase tensor2);
pair<vector_f64, vector_i16> Pow(DoubleTensorBase tensor1, Int64TensorBase tensor2);
pair<vector_f64, vector_i16> Pow(DoubleTensorBase tensor1, FloatTensorBase tensor2);
pair<vector_f32, vector_i16> Pow(Int32TensorBase tensor1, FloatTensorBase tensor2);
pair<vector_f32, vector_i16> Pow(Int64TensorBase tensor1, FloatTensorBase tensor2);
pair<vector_f64, vector_i16> Pow(Int32TensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_f64, vector_i16> Pow(Int64TensorBase tensor1, DoubleTensorBase tensor2);

pair<vector_bool, vector_i16> Eq(FloatTensorBase tensor1, FloatTensorBase tensor2);
pair<vector_bool, vector_i16> Eq(DoubleTensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_bool, vector_i16> Eq(Int32TensorBase tensor1, Int32TensorBase tensor2);
pair<vector_bool, vector_i16> Eq(Int64TensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Eq(BoolTensorBase tensor1, BoolTensorBase tensor2);
pair<vector_bool, vector_i16> Eq(FloatTensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_bool, vector_i16> Eq(Int32TensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Eq(FloatTensorBase tensor1, Int32TensorBase tensor2);
pair<vector_bool, vector_i16> Eq(DoubleTensorBase tensor1, Int32TensorBase tensor2);
pair<vector_bool, vector_i16> Eq(FloatTensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Eq(DoubleTensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Eq(DoubleTensorBase tensor1, FloatTensorBase tensor2);
pair<vector_bool, vector_i16> Eq(Int32TensorBase tensor1, FloatTensorBase tensor2);
pair<vector_bool, vector_i16> Eq(Int64TensorBase tensor1, FloatTensorBase tensor2);
pair<vector_bool, vector_i16> Eq(Int32TensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_bool, vector_i16> Eq(Int64TensorBase tensor1, DoubleTensorBase tensor2);

pair<vector_bool, vector_i16> Gt(FloatTensorBase tensor1, FloatTensorBase tensor2);
pair<vector_bool, vector_i16> Gt(DoubleTensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_bool, vector_i16> Gt(Int32TensorBase tensor1, Int32TensorBase tensor2);
pair<vector_bool, vector_i16> Gt(Int64TensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Gt(BoolTensorBase tensor1, BoolTensorBase tensor2);
pair<vector_bool, vector_i16> Gt(FloatTensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_bool, vector_i16> Gt(Int32TensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Gt(FloatTensorBase tensor1, Int32TensorBase tensor2);
pair<vector_bool, vector_i16> Gt(DoubleTensorBase tensor1, Int32TensorBase tensor2);
pair<vector_bool, vector_i16> Gt(FloatTensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Gt(DoubleTensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Gt(DoubleTensorBase tensor1, FloatTensorBase tensor2);
pair<vector_bool, vector_i16> Gt(Int32TensorBase tensor1, FloatTensorBase tensor2);
pair<vector_bool, vector_i16> Gt(Int64TensorBase tensor1, FloatTensorBase tensor2);
pair<vector_bool, vector_i16> Gt(Int32TensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_bool, vector_i16> Gt(Int64TensorBase tensor1, DoubleTensorBase tensor2);

pair<vector_bool, vector_i16> Lt(FloatTensorBase tensor1, FloatTensorBase tensor2);
pair<vector_bool, vector_i16> Lt(DoubleTensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_bool, vector_i16> Lt(Int32TensorBase tensor1, Int32TensorBase tensor2);
pair<vector_bool, vector_i16> Lt(Int64TensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Lt(BoolTensorBase tensor1, BoolTensorBase tensor2);
pair<vector_bool, vector_i16> Lt(FloatTensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_bool, vector_i16> Lt(Int32TensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Lt(FloatTensorBase tensor1, Int32TensorBase tensor2);
pair<vector_bool, vector_i16> Lt(DoubleTensorBase tensor1, Int32TensorBase tensor2);
pair<vector_bool, vector_i16> Lt(FloatTensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Lt(DoubleTensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Lt(DoubleTensorBase tensor1, FloatTensorBase tensor2);
pair<vector_bool, vector_i16> Lt(Int32TensorBase tensor1, FloatTensorBase tensor2);
pair<vector_bool, vector_i16> Lt(Int64TensorBase tensor1, FloatTensorBase tensor2);
pair<vector_bool, vector_i16> Lt(Int32TensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_bool, vector_i16> Lt(Int64TensorBase tensor1, DoubleTensorBase tensor2);

pair<vector_bool, vector_i16> Ge(FloatTensorBase tensor1, FloatTensorBase tensor2);
pair<vector_bool, vector_i16> Ge(DoubleTensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_bool, vector_i16> Ge(Int32TensorBase tensor1, Int32TensorBase tensor2);
pair<vector_bool, vector_i16> Ge(Int64TensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Ge(BoolTensorBase tensor1, BoolTensorBase tensor2);
pair<vector_bool, vector_i16> Ge(FloatTensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_bool, vector_i16> Ge(Int32TensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Ge(FloatTensorBase tensor1, Int32TensorBase tensor2);
pair<vector_bool, vector_i16> Ge(DoubleTensorBase tensor1, Int32TensorBase tensor2);
pair<vector_bool, vector_i16> Ge(FloatTensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Ge(DoubleTensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Ge(DoubleTensorBase tensor1, FloatTensorBase tensor2);
pair<vector_bool, vector_i16> Ge(Int32TensorBase tensor1, FloatTensorBase tensor2);
pair<vector_bool, vector_i16> Ge(Int64TensorBase tensor1, FloatTensorBase tensor2);
pair<vector_bool, vector_i16> Ge(Int32TensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_bool, vector_i16> Ge(Int64TensorBase tensor1, DoubleTensorBase tensor2);

pair<vector_bool, vector_i16> Le(FloatTensorBase tensor1, FloatTensorBase tensor2);
pair<vector_bool, vector_i16> Le(DoubleTensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_bool, vector_i16> Le(Int32TensorBase tensor1, Int32TensorBase tensor2);
pair<vector_bool, vector_i16> Le(Int64TensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Le(BoolTensorBase tensor1, BoolTensorBase tensor2);
pair<vector_bool, vector_i16> Le(FloatTensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_bool, vector_i16> Le(Int32TensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Le(FloatTensorBase tensor1, Int32TensorBase tensor2);
pair<vector_bool, vector_i16> Le(DoubleTensorBase tensor1, Int32TensorBase tensor2);
pair<vector_bool, vector_i16> Le(FloatTensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Le(DoubleTensorBase tensor1, Int64TensorBase tensor2);
pair<vector_bool, vector_i16> Le(DoubleTensorBase tensor1, FloatTensorBase tensor2);
pair<vector_bool, vector_i16> Le(Int32TensorBase tensor1, FloatTensorBase tensor2);
pair<vector_bool, vector_i16> Le(Int64TensorBase tensor1, FloatTensorBase tensor2);
pair<vector_bool, vector_i16> Le(Int32TensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_bool, vector_i16> Le(Int64TensorBase tensor1, DoubleTensorBase tensor2);

pair<vector_f32, vector_i16> Sum(FloatTensorBase tensor, int32_t dim, bool keepdims);
pair<vector_f64, vector_i16> Sum(DoubleTensorBase tensor, int32_t dim, bool keepdims);
pair<vector_f32, vector_i16> Sum(Int32TensorBase tensor, int32_t dim, bool keepdims);
pair<vector_f64, vector_i16> Sum(Int64TensorBase tensor, int32_t dim, bool keepdims);

pair<vector_f32, vector_i16> Mean(FloatTensorBase tensor, int32_t dim, bool keepdims);
pair<vector_f64, vector_i16> Mean(DoubleTensorBase tensor, int32_t dim, bool keepdims);
pair<vector_f32, vector_i16> Mean(Int32TensorBase tensor, int32_t dim, bool keepdims);
pair<vector_f64, vector_i16> Mean(Int64TensorBase tensor, int32_t dim, bool keepdims);

pair<vector_f32, vector_i16> Median(FloatTensorBase tensor, int32_t dim, bool keepdims);
pair<vector_f64, vector_i16> Median(DoubleTensorBase tensor, int32_t dim, bool keepdims);
pair<vector_f32, vector_i16> Median(Int32TensorBase tensor, int32_t dim, bool keepdims);
pair<vector_f64, vector_i16> Median(Int64TensorBase tensor, int32_t dim, bool keepdims);

pair<vector_f32, vector_i16> Min(FloatTensorBase tensor, int32_t dim, bool keepdims);
pair<vector_f64, vector_i16> Min(DoubleTensorBase tensor, int32_t dim, bool keepdims);
pair<vector_f32, vector_i16> Min(Int32TensorBase tensor, int32_t dim, bool keepdims);
pair<vector_f64, vector_i16> Min(Int64TensorBase tensor, int32_t dim, bool keepdims);

pair<vector_f32, vector_i16> Max(FloatTensorBase tensor, int32_t dim, bool keepdims);
pair<vector_f64, vector_i16> Max(DoubleTensorBase tensor, int32_t dim, bool keepdims);
pair<vector_f32, vector_i16> Max(Int32TensorBase tensor, int32_t dim, bool keepdims);
pair<vector_f64, vector_i16> Max(Int64TensorBase tensor, int32_t dim, bool keepdims);

vector_i16 calculate_stride(vector_i16 shape, int32_t ndim);
int32_t calculate_size(vector_i16 shape, int32_t ndim);
vector_i16 broadcast_stride(vector_i16 shape, vector_i16 stride, int32_t dim, int32_t max_dim);
vector_i16 broadcast_shape(vector_i16 shape1, vector_i16 shape2, int32_t dim1, int32_t dim2, int32_t max_dim);
void update_offset(int32_t *offset1, int32_t *offset2, int32_t *n_idx, int32_t max_dim, vector_i16 stride, vector_i16 resut_stride1, vector_i16 resut_stride2);
bool isbroadcast(vector_i16 shape1, vector_i16 shape2, int dim1, int dim2);
bool is_sum_allow(int32_t dim_to_sum, int32_t tensor_dim);
bool is_view_allow(vector_i16 new_view, int32_t size);

vector_i16 matmul_broadcast_shape(vector_i16 shape1, vector_i16 shape2, int32_t dim1, int32_t dim2);
bool is_matmul_broadcast(vector_i16 shape1, vector_i16 shape2, int32_t dim1, int32_t dim2);
pair<vector_f32, vector_i16> Matmul(FloatTensorBase tensor1, FloatTensorBase tensor2);
pair<vector_f64, vector_i16> Matmul(DoubleTensorBase tensor1, DoubleTensorBase tensor2);
pair<vector_i32, vector_i16> Matmul(Int32TensorBase tensor1, Int32TensorBase tensor2);
pair<vector_i64, vector_i16> Matmul(Int64TensorBase tensor1, Int64TensorBase tensor2);
pair<vector_f32, vector_i16> Trans(FloatTensorBase tensor, int32_t dim0, int32_t dim1);
pair<vector_f64, vector_i16> Trans(DoubleTensorBase tenosr, int32_t dim0, int32_t dim1);
pair<vector_i32, vector_i16> Trans(Int32TensorBase tensor, int32_t dim0, int32_t dim1);
pair<vector_i64, vector_i16> Trans(Int64TensorBase tenosr, int32_t dim0, int32_t dim1);
pair<vector_bool, vector_i16> Trans(BoolTensorBase tensor, int32_t dim0, int32_t dim1);

pair<vector_f32, vector_i16> View(FloatTensorBase tensor, vector_i16 rearrenge_view);
pair<vector_f64, vector_i16> View(DoubleTensorBase tensor, vector_i16 rearrenge_view);
pair<vector_i32, vector_i16> View(Int32TensorBase tensor, vector_i16 rearrenge_view);
pair<vector_i64, vector_i16> View(Int64TensorBase tensor, vector_i16 rearrenge_view);
pair<vector_bool, vector_i16> View(BoolTensorBase tensor, vector_i16 rearrenge_view);


#endif