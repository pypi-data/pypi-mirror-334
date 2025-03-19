#ifndef UTILS_HPP
#define UTILS_HPP

#include "generator.hpp"
#include <utility>

//random_num.cpp
pair<vector_f32, vector_i16> randFloat32(vector_i16 shape, Generator *generator);
pair<vector_f64, vector_i16> randFloat64(vector_i16 shape, Generator *generator);

pair<vector_i32, vector_i16> randintInt32(vector_i16 shape, int32_t low, int32_t high, Generator *generator);
pair<vector_i64, vector_i16> randintInt64(vector_i16 shape, int32_t low, int32_t high, Generator *generator);

pair<vector_f32, vector_i16> zerosFloat32(vector_i16 shape);
pair<vector_f64, vector_i16> zerosFloat64(vector_i16 shape);
pair<vector_i32, vector_i16> zerosInt32(vector_i16 shape);
pair<vector_i64, vector_i16> zerosInt64(vector_i16 shape);

pair<vector_f32, vector_i16> onesFloat32(vector_i16 shape);
pair<vector_f64, vector_i16> onesFloat64(vector_i16 shape);
pair<vector_i32, vector_i16> onesInt32(vector_i16 shape);
pair<vector_i64, vector_i16> onesInt64(vector_i16 shape);

pair<vector_f32, vector_i16> LogFloat32(FloatTensorBase tensor1);
pair<vector_f64, vector_i16> LogFloat64(DoubleTensorBase tensor1);
pair<vector_f32, vector_i16> LogInt32(Int32TensorBase tensor1);
pair<vector_f64, vector_i16> LogInt64(Int64TensorBase tensor1);

pair<vector_f32, vector_i16> Log10Float32(FloatTensorBase tensor1);
pair<vector_f64, vector_i16> Log10Float64(DoubleTensorBase tensor1);
pair<vector_f32, vector_i16> Log10Int32(Int32TensorBase tensor1);
pair<vector_f64, vector_i16> Log10Int64(Int64TensorBase tensor1);

pair<vector_f32, vector_i16> Log2Float32(FloatTensorBase tensor1);
pair<vector_f64, vector_i16> Log2Float64(DoubleTensorBase tensor1);
pair<vector_f32, vector_i16> Log2Int32(Int32TensorBase tensor1);
pair<vector_f64, vector_i16> Log2Int64(Int64TensorBase tensor1);

pair<vector_f32, vector_i16> ExpFloat32(FloatTensorBase tensor1);
pair<vector_f64, vector_i16> ExpFloat64(DoubleTensorBase tensor1);
pair<vector_f32, vector_i16> ExpInt32(Int32TensorBase tensor1);
pair<vector_f64, vector_i16> ExpInt64(Int64TensorBase tensor1);

pair<vector_f32, vector_i16> Exp2Float32(FloatTensorBase tensor1);
pair<vector_f64, vector_i16> Exp2Float64(DoubleTensorBase tensor1);
pair<vector_f32, vector_i16> Exp2Int32(Int32TensorBase tensor1);
pair<vector_f64, vector_i16> Exp2Int64(Int64TensorBase tensor1);

#endif