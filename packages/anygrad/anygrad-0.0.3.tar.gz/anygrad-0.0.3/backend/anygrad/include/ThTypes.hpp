#ifndef THTYPES_HPP
#define THTYPES_HPP

#include <vector>
#include <utility>
#include <functional>
#include <set>
#include <string>

#define vector_f32 vector<float>
#define vector_f64 vector<double>
#define vector_i16 vector<int16_t>
#define vector_i32 vector<int32_t>
#define vector_i64 vector<int64_t>
#define vector_bool vector<bool>

using namespace std;

class BaseTensor{
    public:
        vector_i16 shape;
        vector_i16 stride;
        int32_t ndim;
        int32_t size;
        BaseTensor(vector_i16 shape);
};

class FloatTensorBase : public BaseTensor{
    public:
        vector_f32 data;
        string dtype;
        FloatTensorBase(vector_f32 data, vector_i16 shape);
};

class DoubleTensorBase : public BaseTensor{
    public:
        vector_f64 data;
        string dtype;
        DoubleTensorBase(vector_f64 data, vector_i16 shape);
};

class Int32TensorBase : public BaseTensor {
    public:
        vector_i32 data;
        string dtype;
        Int32TensorBase(vector_i32 data, vector_i16 shape);
};

class Int64TensorBase : public BaseTensor {
    public:
        vector_i64 data;
        string dtype;
        Int64TensorBase(vector_i64 data, vector_i16 shape);
};

class BoolTensorBase : public BaseTensor {
    public:
        vector_bool data;
        string dtype;
        BoolTensorBase(vector_bool data, vector_i16 shape);
};

#endif