#include <algorithm>
#include <limits>
#include <vector>
#include <utility>

#include "../include/ThTypes.hpp"
#include "../include/Th.hpp"

using namespace std;
enum class Ops { SUM, MEAN, MEDIAN, MIN, MAX };

template <typename U, typename V>
pair<V, vector_i16> ReduceConfig(U& tensor, Ops op, int32_t dim, bool keepdims) {
    V result_data;
    vector_i16 result_shape;
    int32_t total_ele = tensor.size;

    using T = typename V::value_type;
    
    if (dim == -1) {
        // in this we init the value by 0 if it's SUM, MEAN, MEDIAN and otherwise
        // for MIN it's infinity
        // for MAX it's -infinity
        T init_val = (op == Ops::MIN) ? numeric_limits<T>::infinity() : 
                     (op == Ops::MAX) ? -numeric_limits<T>::infinity() : 0;
        
        result_data.resize(1, init_val); // then initalize the data with that value for size 1
        
        vector<T> vals; // median vector to get that collect the all terms 
        // then we can use this vals in median caclulation
        // odd numbers = vals[(n+1) / 2]
        // even numbers = vals[(n/2+1)] + vals[(n/2)] / 2
        
        for (int32_t i = 0; i < total_ele; i++) {
            T val = static_cast<T>(tensor.data[i]);
            if (op == Ops::MEDIAN) {
                vals.push_back(val);
            } else if (op == Ops::SUM || op == Ops::MEAN) {
                result_data[0] += val;
            } else if (op == Ops::MIN) {
                result_data[0] = min(result_data[0], val);
            } else if (op == Ops::MAX) {
                result_data[0] = max(result_data[0], val);
            }
        }
        
        if (op == Ops::MEAN) result_data[0] /= total_ele;
        else if (op == Ops::MEDIAN) {
            sort(vals.begin(), vals.end());
            int32_t temp = total_ele / 2;
            if (total_ele % 2 == 0)
                result_data[0] = (vals[temp - 1] + vals[temp]) / 2;
            else
                result_data[0] = vals[temp];
        }
        
        result_shape = keepdims ? vector_i16(tensor.ndim, 1) : vector_i16{1};
        return {result_data, result_shape};
    }
    
    if (keepdims) {
        result_shape = tensor.shape;
        result_shape[dim] = 1;
    } else {
        //this condition is handle the case when we have the tensor shape of 3D after reduction it's can be become the 2D tensor
        // so accourding to we need to change the shape
        result_shape.reserve(tensor.ndim - 1);
        for (int32_t i = 0; i < tensor.ndim; i++)
            if (i != dim) result_shape.push_back(tensor.shape[i]);
        if (result_shape.empty()) result_shape.push_back(1);
    }
    
    int32_t result_size = calculate_size(result_shape, result_shape.size());
    int32_t reduce_dim_size = tensor.shape[dim];
    result_data.resize(result_size);
    
    if (op != Ops::MEDIAN) {
        T init_val = (op == Ops::MIN) ? numeric_limits<T>::infinity() : 
                    (op == Ops::MAX) ? -numeric_limits<T>::infinity() : 0;
        fill(result_data.begin(), result_data.end(), init_val);
        // now this time we have the vector so we inti the hole vector with init_val
    }
    
    vector_i16 out_stride = calculate_stride(result_shape, result_shape.size());
    
    vector<vector<T>> median_val;
    if (op == Ops::MEDIAN) {
        median_val.resize(result_size);
        for (auto& v : median_val) v.reserve(reduce_dim_size);
    }
    
    //go thorugh the total_elements and calculate the op.
    for (int32_t idx = 0; idx < total_ele; idx++) {
        int32_t ind = 0;
        for (int32_t d = 0, rd = 0; d < tensor.ndim; d++) {
            if (d == dim) continue;
            int32_t offset = (idx / tensor.stride[d]) % tensor.shape[d];
            ind += offset * out_stride[rd++];
        }
        
        T value = static_cast<T>(tensor.data[idx]);
        
        if (op == Ops::MEDIAN) {
            median_val[ind].push_back(value);
        } else if (op == Ops::SUM || op == Ops::MEAN) {
            result_data[ind] += value;
        } else if (op == Ops::MIN) {
            result_data[ind] = min(result_data[ind], value);
        } else if (op == Ops::MAX) {
            result_data[ind] = max(result_data[ind], value);
        }
    }
    
    if (op == Ops::MEAN) {
        for (int32_t i = 0; i < result_size; i++)
            result_data[i] /= reduce_dim_size;
    } else if (op == Ops::MEDIAN) {
        for (int32_t i = 0; i < result_size; i++) {
            auto& vals = median_val[i];
            sort(vals.begin(), vals.end());
            if (vals.size() % 2 == 0)
                result_data[i] = (vals[vals.size()/2 - 1] + vals[vals.size()/2]) / 2;
            else
                result_data[i] = vals[vals.size() / 2];
        }
    }
    
    return {result_data, result_shape};
}

template <typename T1, typename T2, typename U, typename Op>
pair<U, vector_i16> BaseConfigOp(T1 tensor1, T2 tensor2, Op op){
    // for scaler tensor
    if (tensor2.size == 1){
        U result_data(tensor1.size, 0);
        for (int i = 0; i < tensor1.size; i ++){
            result_data[i] = op(tensor1.data[i], tensor2.data[0]);
        }
        return {result_data, tensor1.shape};
    }

    int32_t max_dim = max(tensor1.ndim, tensor2.ndim);

    vector_i16 result_stride1 = broadcast_stride(tensor1.shape, tensor1.stride, tensor1.ndim, max_dim);
    vector_i16 result_stride2 = broadcast_stride(tensor2.shape, tensor2.stride, tensor2.ndim, max_dim);

    vector_i16 result_shape = broadcast_shape(tensor1.shape, tensor2.shape, tensor1.ndim, tensor2.ndim, max_dim);
    int32_t total_ele = calculate_size(result_shape, result_shape.size());
    vector_i16 result_stride = calculate_stride(result_shape, result_shape.size());

    U result_data(total_ele);

    for(int32_t idx = 0; idx < total_ele; idx++){
        int32_t offset1 = 0; int32_t offset2 = 0;
        int n_idx = idx;

        update_offset(&offset1, &offset2, &n_idx, max_dim, result_stride, result_stride1, result_stride2);
        result_data[idx] = op(tensor1.data[offset1],tensor2.data[offset2]);
    }

    //I think this is the best way to delete the vector
    vector_i16().swap(result_stride1);
    vector_i16().swap(result_stride2);
    vector_i16().swap(result_stride);

    return {result_data, result_shape};
}

// ---------------------------------------- Sorry, I could not find the other way to declare this :( ---------------------------------------- //

// -------------------Add---------------------
pair<vector_f32, vector_i16> Add(FloatTensorBase tensor1, FloatTensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, FloatTensorBase, vector_f32, function<float(float, float)>>(tensor1,tensor2, 
    [](float num1, float num2) {return num1 + num2;});
}

pair<vector_f64, vector_i16> Add(DoubleTensorBase tensor1, DoubleTensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, DoubleTensorBase, vector_f64, function<double(double, double)>>(tensor1,tensor2, 
    [](double num1, double num2) {return num1 + num2;});   
}

pair<vector_i32, vector_i16> Add(Int32TensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<Int32TensorBase, Int32TensorBase, vector_i32, function<int32_t(int32_t, int32_t)>>(tensor1,tensor2, 
    [](int32_t num1, int32_t num2) {return num1 + num2;});
}

pair<vector_i64, vector_i16> Add(Int64TensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<Int64TensorBase, Int64TensorBase, vector_i64, function<int64_t(int64_t, int64_t)>>(tensor1,tensor2, 
    [](int64_t num1, int64_t num2) {return num1 + num2;});
}

pair<vector_bool, vector_i16> Add(BoolTensorBase tensor1, BoolTensorBase tensor2){
    return BaseConfigOp<BoolTensorBase, BoolTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) {return num1 + num2;});
}

pair<vector_f64, vector_i16> Add(FloatTensorBase tensor1, DoubleTensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, DoubleTensorBase, vector_f64, function<double(float, double)>>(tensor1, tensor2,
    [](float num1, double num2) {return static_cast<double>(num1) + num2;});
}

pair<vector_i64, vector_i16> Add(Int32TensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<Int32TensorBase, Int64TensorBase, vector_i64, function<int64_t(float, double)>>(tensor1, tensor2,
        [](float num1, int64_t num2) {return static_cast<int64_t>(num1) + num2;});
}

pair<vector_f32, vector_i16> Add(FloatTensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, Int32TensorBase, vector_f32, function<float(float, int32_t)>>(tensor1, tensor2,
        [](float num1, int32_t num2) {return num1 + static_cast<float>(num2);});
}

pair<vector_f64, vector_i16> Add(DoubleTensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, Int32TensorBase, vector_f64, function<double(double, int32_t)>>(tensor1, tensor2,
        [](double num1, int32_t num2) {return static_cast<double>(num1) + num2;});
}

pair<vector_f32, vector_i16> Add(FloatTensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, Int64TensorBase, vector_f32, function<float(double, int64_t)>>(tensor1, tensor2,
        [](double num1, int64_t num2) {return static_cast<double>(num1) + num2;});
}
pair<vector_f64, vector_i16> Add(DoubleTensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, Int64TensorBase, vector_f64, function<double(double, int64_t)>>(tensor1, tensor2,
        [](double num1, int64_t num2) {return static_cast<double>(num1) + num2;});
}

pair<vector_f64, vector_i16> Add(DoubleTensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<DoubleTensorBase, FloatTensorBase, vector_f64, function<double(double, float)>>(tensor1, tensor2,
        [](double num1, float num2) {return num1 + num2;});
}

pair<vector_f32, vector_i16> Add(Int32TensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<Int32TensorBase, FloatTensorBase, vector_f32, function<float(int32_t, float)>>(tensor1, tensor2,
        [](int32_t num1, float num2) {return static_cast<float>(num1) + num2;});
}

pair<vector_f32, vector_i16> Add(Int64TensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<Int64TensorBase, FloatTensorBase, vector_f32, function<float(int64_t, float)>>(tensor1, tensor2,
        [](int64_t num1, float num2) {return static_cast<float>(num1) + num2;});
}

pair<vector_f64, vector_i16> Add(Int32TensorBase tensor1, DoubleTensorBase tensor2) {
    return BaseConfigOp<Int32TensorBase, DoubleTensorBase, vector_f64, function<double(int32_t, double)>>(tensor1, tensor2,
        [](int32_t num1, double num2) {return static_cast<double>(num1) + num2;});
}

pair<vector_f64, vector_i16> Add(Int64TensorBase tensor1, DoubleTensorBase tensor2) {
    return BaseConfigOp<Int64TensorBase, DoubleTensorBase, vector_f64, function<double(int64_t, double)>>(tensor1, tensor2,
        [](int64_t num1, double num2) {return static_cast<double>(num1) + num2;});
}

// -------------------Sub---------------------
pair<vector_f32, vector_i16> Sub(FloatTensorBase tensor1, FloatTensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, FloatTensorBase, vector_f32, function<float(float, float)>>(tensor1,tensor2, 
    [](float num1, float num2) {return num1 - num2;});
}

pair<vector_f64, vector_i16> Sub(DoubleTensorBase tensor1, DoubleTensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, DoubleTensorBase, vector_f64, function<double(double, double)>>(tensor1,tensor2, 
    [](double num1, double num2) {return num1 - num2;});   
}

pair<vector_i32, vector_i16> Sub(Int32TensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<Int32TensorBase, Int32TensorBase, vector_i32, function<int32_t(int32_t, int32_t)>>(tensor1,tensor2, 
    [](int32_t num1, int32_t num2) {return num1 - num2;});
}

pair<vector_i64, vector_i16> Sub(Int64TensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<Int64TensorBase, Int64TensorBase, vector_i64, function<int64_t(int64_t, int64_t)>>(tensor1,tensor2, 
    [](int64_t num1, int64_t num2) {return num1 - num2;});
}

pair<vector_bool, vector_i16> Sub(BoolTensorBase tensor1, BoolTensorBase tensor2){
    return BaseConfigOp<BoolTensorBase, BoolTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) {return num1 - num2;});
}

pair<vector_f64, vector_i16> Sub(FloatTensorBase tensor1, DoubleTensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, DoubleTensorBase, vector_f64, function<double(float, double)>>(tensor1, tensor2,
    [](float num1, double num2) {return static_cast<double>(num1) - num2;});
}

pair<vector_i64, vector_i16> Sub(Int32TensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<Int32TensorBase, Int64TensorBase, vector_i64, function<int64_t(float, double)>>(tensor1, tensor2,
        [](float num1, int64_t num2) {return static_cast<int64_t>(num1) - num2;});
}

pair<vector_f32, vector_i16> Sub(FloatTensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, Int32TensorBase, vector_f32, function<float(float, int32_t)>>(tensor1, tensor2,
        [](float num1, int32_t num2) {return num1 - static_cast<float>(num2);});
}

pair<vector_f64, vector_i16> Sub(DoubleTensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, Int32TensorBase, vector_f64, function<double(double, int32_t)>>(tensor1, tensor2,
        [](double num1, int32_t num2) {return static_cast<double>(num1) - num2;});
}

pair<vector_f32, vector_i16> Sub(FloatTensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, Int64TensorBase, vector_f32, function<float(double, int64_t)>>(tensor1, tensor2,
        [](double num1, int64_t num2) {return static_cast<double>(num1) - num2;});
}
pair<vector_f64, vector_i16> Sub(DoubleTensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, Int64TensorBase, vector_f64, function<double(double, int64_t)>>(tensor1, tensor2,
        [](double num1, int64_t num2) {return static_cast<double>(num1) - num2;});
}

pair<vector_f64, vector_i16> Sub(DoubleTensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<DoubleTensorBase, FloatTensorBase, vector_f64, function<double(double, float)>>(tensor1, tensor2,
        [](double num1, float num2) {return num1 - num2;});
}

pair<vector_f32, vector_i16> Sub(Int32TensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<Int32TensorBase, FloatTensorBase, vector_f32, function<float(int32_t, float)>>(tensor1, tensor2,
        [](int32_t num1, float num2) {return static_cast<float>(num1) - num2;});
}

pair<vector_f32, vector_i16> Sub(Int64TensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<Int64TensorBase, FloatTensorBase, vector_f32, function<float(int64_t, float)>>(tensor1, tensor2,
        [](int64_t num1, float num2) {return static_cast<float>(num1) - num2;});
}

pair<vector_f64, vector_i16> Sub(Int32TensorBase tensor1, DoubleTensorBase tensor2) {
    return BaseConfigOp<Int32TensorBase, DoubleTensorBase, vector_f64, function<double(int32_t, double)>>(tensor1, tensor2,
        [](int32_t num1, double num2) {return static_cast<double>(num1) - num2;});
}

pair<vector_f64, vector_i16> Sub(Int64TensorBase tensor1, DoubleTensorBase tensor2) {
    return BaseConfigOp<Int64TensorBase, DoubleTensorBase, vector_f64, function<double(int64_t, double)>>(tensor1, tensor2,
        [](int64_t num1, double num2) {return static_cast<double>(num1) - num2;});
}

// -------------------Mul---------------------

pair<vector_f32, vector_i16> Mul(FloatTensorBase tensor1, FloatTensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, FloatTensorBase, vector_f32, function<float(float, float)>>(tensor1,tensor2, 
    [](float num1, float num2) {return num1 * num2;});
}

pair<vector_f64, vector_i16> Mul(DoubleTensorBase tensor1, DoubleTensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, DoubleTensorBase, vector_f64, function<double(double, double)>>(tensor1,tensor2, 
    [](double num1, double num2) {return num1 * num2;});   
}

pair<vector_i32, vector_i16> Mul(Int32TensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<Int32TensorBase, Int32TensorBase, vector_i32, function<int32_t(int32_t, int32_t)>>(tensor1,tensor2, 
    [](int32_t num1, int32_t num2) {return num1 * num2;});
}

pair<vector_i64, vector_i16> Mul(Int64TensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<Int64TensorBase, Int64TensorBase, vector_i64, function<int64_t(int64_t, int64_t)>>(tensor1,tensor2, 
    [](int64_t num1, int64_t num2) {return num1 * num2;});
}

pair<vector_bool, vector_i16> Mul(BoolTensorBase tensor1, BoolTensorBase tensor2){
    return BaseConfigOp<BoolTensorBase, BoolTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) {return num1 * num2;});
}

pair<vector_f64, vector_i16> Mul(FloatTensorBase tensor1, DoubleTensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, DoubleTensorBase, vector_f64, function<double(float, double)>>(tensor1, tensor2,
    [](float num1, double num2) {return static_cast<double>(num1) * num2;});
}

pair<vector_i64, vector_i16> Mul(Int32TensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<Int32TensorBase, Int64TensorBase, vector_i64, function<int64_t(float, double)>>(tensor1, tensor2,
        [](float num1, int64_t num2) {return static_cast<int64_t>(num1) * num2;});
}

pair<vector_f32, vector_i16> Mul(FloatTensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, Int32TensorBase, vector_f32, function<float(float, int32_t)>>(tensor1, tensor2,
        [](float num1, int32_t num2) {return num1 * static_cast<float>(num2);});
}

pair<vector_f64, vector_i16> Mul(DoubleTensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, Int32TensorBase, vector_f64, function<double(double, int32_t)>>(tensor1, tensor2,
        [](double num1, int32_t num2) {return static_cast<double>(num1) * num2;});
}

pair<vector_f32, vector_i16> Mul(FloatTensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, Int64TensorBase, vector_f32, function<float(double, int64_t)>>(tensor1, tensor2,
        [](double num1, int64_t num2) {return static_cast<double>(num1) * num2;});
}
pair<vector_f64, vector_i16> Mul(DoubleTensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, Int64TensorBase, vector_f64, function<double(double, int64_t)>>(tensor1, tensor2,
        [](double num1, int64_t num2) {return static_cast<double>(num1) * num2;});
}

pair<vector_f64, vector_i16> Mul(DoubleTensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<DoubleTensorBase, FloatTensorBase, vector_f64, function<double(double, float)>>(tensor1, tensor2,
        [](double num1, float num2) {return num1 * num2;});
}

pair<vector_f32, vector_i16> Mul(Int32TensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<Int32TensorBase, FloatTensorBase, vector_f32, function<float(int32_t, float)>>(tensor1, tensor2,
        [](int32_t num1, float num2) {return static_cast<float>(num1) * num2;});
}

pair<vector_f32, vector_i16> Mul(Int64TensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<Int64TensorBase, FloatTensorBase, vector_f32, function<float(int64_t, float)>>(tensor1, tensor2,
        [](int64_t num1, float num2) {return static_cast<float>(num1) * num2;});
}

pair<vector_f64, vector_i16> Mul(Int32TensorBase tensor1, DoubleTensorBase tensor2) {
    return BaseConfigOp<Int32TensorBase, DoubleTensorBase, vector_f64, function<double(int32_t, double)>>(tensor1, tensor2,
        [](int32_t num1, double num2) {return static_cast<double>(num1) * num2;});
}

pair<vector_f64, vector_i16> Mul(Int64TensorBase tensor1, DoubleTensorBase tensor2) {
    return BaseConfigOp<Int64TensorBase, DoubleTensorBase, vector_f64, function<double(int64_t, double)>>(tensor1, tensor2,
        [](int64_t num1, double num2) {return static_cast<double>(num1) * num2;});
}

// -------------------Div---------------------
pair<vector_f32, vector_i16> Div(FloatTensorBase tensor1, FloatTensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, FloatTensorBase, vector_f32, function<float(float, float)>>(tensor1,tensor2, 
    [](float num1, float num2) {return num1 / num2;});
}

pair<vector_f64, vector_i16> Div(DoubleTensorBase tensor1, DoubleTensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, DoubleTensorBase, vector_f64, function<double(double, double)>>(tensor1,tensor2, 
    [](double num1, double num2) {return num1 / num2;});   
}

pair<vector_f32, vector_i16> Div(Int32TensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<Int32TensorBase, Int32TensorBase, vector_f32, function<float(int32_t, int32_t)>>(tensor1,tensor2, 
    [](int32_t num1, int32_t num2) {return static_cast<float>(num1) / static_cast<float>(num2);});
}

pair<vector_f64, vector_i16> Div(Int64TensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<Int64TensorBase, Int64TensorBase, vector_f64, function<double(int64_t, int64_t)>>(tensor1,tensor2, 
    [](int64_t num1, int64_t num2) {return static_cast<double>(num1) / static_cast<double>(num2);});
}

pair<vector_bool, vector_i16> Div(BoolTensorBase tensor1, BoolTensorBase tensor2){
    return BaseConfigOp<BoolTensorBase, BoolTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) {return num1 / num2;});
}

pair<vector_f64, vector_i16> Div(FloatTensorBase tensor1, DoubleTensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, DoubleTensorBase, vector_f64, function<double(float, double)>>(tensor1, tensor2,
    [](float num1, double num2) {return static_cast<double>(num1) / num2;});
}

pair<vector_f64, vector_i16> Div(Int32TensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<Int32TensorBase, Int64TensorBase, vector_f64, function<float(int32_t, int64_t)>>(tensor1, tensor2,
        [](int32_t num1, int64_t num2) {return static_cast<double>(num1) / static_cast<double>(num2);});
}

pair<vector_f32, vector_i16> Div(FloatTensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, Int32TensorBase, vector_f32, function<float(float, int32_t)>>(tensor1, tensor2,
        [](float num1, int32_t num2) {return num1 / static_cast<float>(num2);});
}

pair<vector_f64, vector_i16> Div(DoubleTensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, Int32TensorBase, vector_f64, function<double(double, int32_t)>>(tensor1, tensor2,
        [](double num1, int32_t num2) {return static_cast<double>(num1) / num2;});
}

pair<vector_f32, vector_i16> Div(FloatTensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, Int64TensorBase, vector_f32, function<float(double, int64_t)>>(tensor1, tensor2,
        [](double num1, int64_t num2) {return static_cast<double>(num1) / num2;});
}
pair<vector_f64, vector_i16> Div(DoubleTensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, Int64TensorBase, vector_f64, function<double(double, int64_t)>>(tensor1, tensor2,
        [](double num1, int64_t num2) {return static_cast<double>(num1) / num2;});
}

pair<vector_f64, vector_i16> Div(DoubleTensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<DoubleTensorBase, FloatTensorBase, vector_f64, function<double(double, float)>>(tensor1, tensor2,
        [](double num1, float num2) {return num1 / num2;});
}

pair<vector_f32, vector_i16> Div(Int32TensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<Int32TensorBase, FloatTensorBase, vector_f32, function<float(int32_t, float)>>(tensor1, tensor2,
        [](int32_t num1, float num2) {return static_cast<float>(num1) / num2;});
}

pair<vector_f32, vector_i16> Div(Int64TensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<Int64TensorBase, FloatTensorBase, vector_f32, function<float(int64_t, float)>>(tensor1, tensor2,
        [](int64_t num1, float num2) {return static_cast<float>(num1) / num2;});
}

pair<vector_f64, vector_i16> Div(Int32TensorBase tensor1, DoubleTensorBase tensor2) {
    return BaseConfigOp<Int32TensorBase, DoubleTensorBase, vector_f64, function<double(int32_t, double)>>(tensor1, tensor2,
        [](int32_t num1, double num2) {return static_cast<double>(num1) / num2;});
}

pair<vector_f64, vector_i16> Div(Int64TensorBase tensor1, DoubleTensorBase tensor2) {
    return BaseConfigOp<Int64TensorBase, DoubleTensorBase, vector_f64, function<double(int64_t, double)>>(tensor1, tensor2,
        [](int64_t num1, double num2) {return static_cast<double>(num1) / num2;});
}

// -------------------Pow---------------------

pair<vector_f32, vector_i16> Pow(FloatTensorBase tensor1, FloatTensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, FloatTensorBase, vector_f32, function<float(float, float)>>(tensor1,tensor2, 
    [](float num1, float num2) { return pow(num1, num2); });
}

pair<vector_f64, vector_i16> Pow(DoubleTensorBase tensor1, DoubleTensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, DoubleTensorBase, vector_f64, function<double(double, double)>>(tensor1,tensor2, 
    [](double num1, double num2) { return pow(num1, num2); });   
}

pair<vector_i32, vector_i16> Pow(Int32TensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<Int32TensorBase, Int32TensorBase, vector_i32, function<int32_t(int32_t, int32_t)>>(tensor1,tensor2, 
    [](int32_t num1, int32_t num2) { return pow(num1, num2); });
}

pair<vector_i64, vector_i16> Pow(Int64TensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<Int64TensorBase, Int64TensorBase, vector_i64, function<int64_t(int64_t, int64_t)>>(tensor1,tensor2, 
    [](int64_t num1, int64_t num2) { return pow(num1, num2); });
}

pair<vector_bool, vector_i16> Pow(BoolTensorBase tensor1, BoolTensorBase tensor2){
    return BaseConfigOp<BoolTensorBase, BoolTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return pow(num1, num2); });
}

pair<vector_f64, vector_i16> Pow(FloatTensorBase tensor1, DoubleTensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, DoubleTensorBase, vector_f64, function<double(float, double)>>(tensor1, tensor2,
    [](float num1, double num2) { return static_cast<double>(pow(num1, num2)); });
}

pair<vector_i64, vector_i16> Pow(Int32TensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<Int32TensorBase, Int64TensorBase, vector_i64, function<int64_t(float, double)>>(tensor1, tensor2,
        [](float num1, int64_t num2) { return static_cast<int64_t>(pow(num1, num2)); });
}

pair<vector_f32, vector_i16> Pow(FloatTensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, Int32TensorBase, vector_f32, function<float(float, int32_t)>>(tensor1, tensor2,
        [](float num1, int32_t num2) { return pow(num1, static_cast<float>(num2)); });
}

pair<vector_f64, vector_i16> Pow(DoubleTensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, Int32TensorBase, vector_f64, function<double(double, int32_t)>>(tensor1, tensor2,
        [](double num1, int32_t num2) { return static_cast<double>(pow(num1, num2)); });
}

pair<vector_f32, vector_i16> Pow(FloatTensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, Int64TensorBase, vector_f32, function<float(double, int64_t)>>(tensor1, tensor2,
        [](double num1, int64_t num2) { return static_cast<double>(pow(num1, num2)); });
}
pair<vector_f64, vector_i16> Pow(DoubleTensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, Int64TensorBase, vector_f64, function<double(double, int64_t)>>(tensor1, tensor2,
        [](double num1, int64_t num2) { return static_cast<double>(pow(num1, num2)); });
}

pair<vector_f64, vector_i16> Pow(DoubleTensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<DoubleTensorBase, FloatTensorBase, vector_f64, function<double(double, float)>>(tensor1, tensor2,
        [](double num1, float num2) { return pow(num1, num2); });
}

pair<vector_f32, vector_i16> Pow(Int32TensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<Int32TensorBase, FloatTensorBase, vector_f32, function<float(int32_t, float)>>(tensor1, tensor2,
        [](int32_t num1, float num2) { return static_cast<float>(pow(num1, num2)); });
}

pair<vector_f32, vector_i16> Pow(Int64TensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<Int64TensorBase, FloatTensorBase, vector_f32, function<float(int64_t, float)>>(tensor1, tensor2,
        [](int64_t num1, float num2) { return static_cast<float>(pow(num1, num2)); });
}

pair<vector_f64, vector_i16> Pow(Int32TensorBase tensor1, DoubleTensorBase tensor2) {
    return BaseConfigOp<Int32TensorBase, DoubleTensorBase, vector_f64, function<double(int32_t, double)>>(tensor1, tensor2,
        [](int32_t num1, double num2) { return static_cast<double>(pow(num1, num2)); });
}

pair<vector_f64, vector_i16> Pow(Int64TensorBase tensor1, DoubleTensorBase tensor2) {
    return BaseConfigOp<Int64TensorBase, DoubleTensorBase, vector_f64, function<double(int64_t, double)>>(tensor1, tensor2,
        [](int64_t num1, double num2) { return static_cast<double>(pow(num1, num2)); });
}


// -------------------Eq---------------------

pair<vector_bool, vector_i16> Eq(FloatTensorBase tensor1, FloatTensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, FloatTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 == num2; });
}

pair<vector_bool, vector_i16> Eq(DoubleTensorBase tensor1, DoubleTensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, DoubleTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 == num2; });   
}

pair<vector_bool, vector_i16> Eq(Int32TensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<Int32TensorBase, Int32TensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 == num2; });
}

pair<vector_bool, vector_i16> Eq(Int64TensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<Int64TensorBase, Int64TensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 == num2; });
}

pair<vector_bool, vector_i16> Eq(BoolTensorBase tensor1, BoolTensorBase tensor2){
    return BaseConfigOp<BoolTensorBase, BoolTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 == num2; });
}

pair<vector_bool, vector_i16> Eq(FloatTensorBase tensor1, DoubleTensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, DoubleTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1, tensor2,
    [](bool num1, bool num2) { return num1 == num2; });
}

pair<vector_bool, vector_i16> Eq(Int32TensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<Int32TensorBase, Int64TensorBase, vector_bool, function<bool(int32_t, int64_t)>>(tensor1, tensor2,
        [](int32_t num1, int64_t num2) { return num1 == num2; });
}

pair<vector_bool, vector_i16> Eq(FloatTensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, Int32TensorBase, vector_bool, function<bool(float, int32_t)>>(tensor1, tensor2,
        [](float num1, int32_t num2) { return num1 == num2; });
}

pair<vector_bool, vector_i16> Eq(DoubleTensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, Int32TensorBase, vector_bool, function<bool(double, int32_t)>>(tensor1, tensor2,
        [](double num1, int32_t num2) { return num1 == num2; });
}

pair<vector_bool, vector_i16> Eq(FloatTensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, Int64TensorBase, vector_bool, function<bool(float, int64_t)>>(tensor1, tensor2,
        [](float num1, int64_t num2) { return num1 == num2; });
}

pair<vector_bool, vector_i16> Eq(DoubleTensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, Int64TensorBase, vector_bool, function<bool(double, int64_t)>>(tensor1, tensor2,
        [](double num1, int64_t num2) { return num1 == num2; });
}

pair<vector_bool, vector_i16> Eq(DoubleTensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<DoubleTensorBase, FloatTensorBase, vector_bool, function<bool(double, float)>>(tensor1, tensor2,
        [](double num1, float num2) { return num1 == num2; });
}

pair<vector_bool, vector_i16> Eq(Int32TensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<Int32TensorBase, FloatTensorBase, vector_bool, function<bool(int32_t, float)>>(tensor1, tensor2,
        [](int32_t num1, float num2) { return num1 == num2; });
}

pair<vector_bool, vector_i16> Eq(Int64TensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<Int64TensorBase, FloatTensorBase, vector_bool, function<bool(int64_t, float)>>(tensor1, tensor2,
        [](int64_t num1, float num2) { return num1 == num2; });
}

pair<vector_bool, vector_i16> Eq(Int32TensorBase tensor1, DoubleTensorBase tensor2) {
    return BaseConfigOp<Int32TensorBase, DoubleTensorBase, vector_bool, function<bool(int32_t, double)>>(tensor1, tensor2,
        [](int32_t num1, double num2) { return num1 == num2; });
}

pair<vector_bool, vector_i16> Eq(Int64TensorBase tensor1, DoubleTensorBase tensor2) {
    return BaseConfigOp<Int64TensorBase, DoubleTensorBase, vector_bool, function<bool(int64_t, double)>>(tensor1, tensor2,
        [](int64_t num1, double num2) { return num1 == num2; });
}

// -------------------Gt---------------------
pair<vector_bool, vector_i16> Gt(FloatTensorBase tensor1, FloatTensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, FloatTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 > num2; });
}

pair<vector_bool, vector_i16> Gt(DoubleTensorBase tensor1, DoubleTensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, DoubleTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 > num2; });   
}

pair<vector_bool, vector_i16> Gt(Int32TensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<Int32TensorBase, Int32TensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 > num2; });
}

pair<vector_bool, vector_i16> Gt(Int64TensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<Int64TensorBase, Int64TensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 > num2; });
}

pair<vector_bool, vector_i16> Gt(BoolTensorBase tensor1, BoolTensorBase tensor2){
    return BaseConfigOp<BoolTensorBase, BoolTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 > num2; });
}

pair<vector_bool, vector_i16> Gt(FloatTensorBase tensor1, DoubleTensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, DoubleTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1, tensor2,
    [](bool num1, bool num2) { return num1 > num2; });
}

pair<vector_bool, vector_i16> Gt(Int32TensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<Int32TensorBase, Int64TensorBase, vector_bool, function<bool(int32_t, int64_t)>>(tensor1, tensor2,
        [](int32_t num1, int64_t num2) { return num1 > num2; });
}

pair<vector_bool, vector_i16> Gt(FloatTensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, Int32TensorBase, vector_bool, function<bool(float, int32_t)>>(tensor1, tensor2,
        [](float num1, int32_t num2) { return num1 > num2; });
}

pair<vector_bool, vector_i16> Gt(DoubleTensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, Int32TensorBase, vector_bool, function<bool(double, int32_t)>>(tensor1, tensor2,
        [](double num1, int32_t num2) { return num1 > num2; });
}

pair<vector_bool, vector_i16> Gt(FloatTensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, Int64TensorBase, vector_bool, function<bool(float, int64_t)>>(tensor1, tensor2,
        [](float num1, int64_t num2) { return num1 > num2; });
}

pair<vector_bool, vector_i16> Gt(DoubleTensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, Int64TensorBase, vector_bool, function<bool(double, int64_t)>>(tensor1, tensor2,
        [](double num1, int64_t num2) { return num1 > num2; });
}

pair<vector_bool, vector_i16> Gt(DoubleTensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<DoubleTensorBase, FloatTensorBase, vector_bool, function<bool(double, float)>>(tensor1, tensor2,
        [](double num1, float num2) { return num1 > num2; });
}

pair<vector_bool, vector_i16> Gt(Int32TensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<Int32TensorBase, FloatTensorBase, vector_bool, function<bool(int32_t, float)>>(tensor1, tensor2,
        [](int32_t num1, float num2) { return num1 > num2; });
}

pair<vector_bool, vector_i16> Gt(Int64TensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<Int64TensorBase, FloatTensorBase, vector_bool, function<bool(int64_t, float)>>(tensor1, tensor2,
        [](int64_t num1, float num2) { return num1 > num2; });
}

pair<vector_bool, vector_i16> Gt(Int32TensorBase tensor1, DoubleTensorBase tensor2) {
    return BaseConfigOp<Int32TensorBase, DoubleTensorBase, vector_bool, function<bool(int32_t, double)>>(tensor1, tensor2,
        [](int32_t num1, double num2) { return num1 > num2; });
}

pair<vector_bool, vector_i16> Gt(Int64TensorBase tensor1, DoubleTensorBase tensor2) {
    return BaseConfigOp<Int64TensorBase, DoubleTensorBase, vector_bool, function<bool(int64_t, double)>>(tensor1, tensor2,
        [](int64_t num1, double num2) { return num1 > num2; });
}

// -------------------Lt---------------------
pair<vector_bool, vector_i16> Lt(FloatTensorBase tensor1, FloatTensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, FloatTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 < num2; });
}

pair<vector_bool, vector_i16> Lt(DoubleTensorBase tensor1, DoubleTensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, DoubleTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 < num2; });   
}

pair<vector_bool, vector_i16> Lt(Int32TensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<Int32TensorBase, Int32TensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 < num2; });
}

pair<vector_bool, vector_i16> Lt(Int64TensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<Int64TensorBase, Int64TensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 < num2; });
}

pair<vector_bool, vector_i16> Lt(BoolTensorBase tensor1, BoolTensorBase tensor2){
    return BaseConfigOp<BoolTensorBase, BoolTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 < num2; });
}

pair<vector_bool, vector_i16> Lt(FloatTensorBase tensor1, DoubleTensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, DoubleTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1, tensor2,
    [](bool num1, bool num2) { return num1 < num2; });
}

pair<vector_bool, vector_i16> Lt(Int32TensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<Int32TensorBase, Int64TensorBase, vector_bool, function<bool(int32_t, int64_t)>>(tensor1, tensor2,
        [](int32_t num1, int64_t num2) { return num1 < num2; });
}

pair<vector_bool, vector_i16> Lt(FloatTensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, Int32TensorBase, vector_bool, function<bool(float, int32_t)>>(tensor1, tensor2,
        [](float num1, int32_t num2) { return num1 < num2; });
}

pair<vector_bool, vector_i16> Lt(DoubleTensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, Int32TensorBase, vector_bool, function<bool(double, int32_t)>>(tensor1, tensor2,
        [](double num1, int32_t num2) { return num1 < num2; });
}

pair<vector_bool, vector_i16> Lt(FloatTensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, Int64TensorBase, vector_bool, function<bool(float, int64_t)>>(tensor1, tensor2,
        [](float num1, int64_t num2) { return num1 < num2; });
}

pair<vector_bool, vector_i16> Lt(DoubleTensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, Int64TensorBase, vector_bool, function<bool(double, int64_t)>>(tensor1, tensor2,
        [](double num1, int64_t num2) { return num1 < num2; });
}

pair<vector_bool, vector_i16> Lt(DoubleTensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<DoubleTensorBase, FloatTensorBase, vector_bool, function<bool(double, float)>>(tensor1, tensor2,
        [](double num1, float num2) { return num1 < num2; });
}

pair<vector_bool, vector_i16> Lt(Int32TensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<Int32TensorBase, FloatTensorBase, vector_bool, function<bool(int32_t, float)>>(tensor1, tensor2,
        [](int32_t num1, float num2) { return num1 < num2; });
}

pair<vector_bool, vector_i16> Lt(Int64TensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<Int64TensorBase, FloatTensorBase, vector_bool, function<bool(int64_t, float)>>(tensor1, tensor2,
        [](int64_t num1, float num2) { return num1 < num2; });
}

pair<vector_bool, vector_i16> Lt(Int32TensorBase tensor1, DoubleTensorBase tensor2) {
    return BaseConfigOp<Int32TensorBase, DoubleTensorBase, vector_bool, function<bool(int32_t, double)>>(tensor1, tensor2,
        [](int32_t num1, double num2) { return num1 < num2; });
}

pair<vector_bool, vector_i16> Lt(Int64TensorBase tensor1, DoubleTensorBase tensor2) {
    return BaseConfigOp<Int64TensorBase, DoubleTensorBase, vector_bool, function<bool(int64_t, double)>>(tensor1, tensor2,
        [](int64_t num1, double num2) { return num1 < num2; });
}

// -------------------Ge---------------------
pair<vector_bool, vector_i16> Ge(FloatTensorBase tensor1, FloatTensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, FloatTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 >= num2; });
}

pair<vector_bool, vector_i16> Ge(DoubleTensorBase tensor1, DoubleTensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, DoubleTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 >= num2; });   
}

pair<vector_bool, vector_i16> Ge(Int32TensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<Int32TensorBase, Int32TensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 >= num2; });
}

pair<vector_bool, vector_i16> Ge(Int64TensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<Int64TensorBase, Int64TensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 >= num2; });
}

pair<vector_bool, vector_i16> Ge(BoolTensorBase tensor1, BoolTensorBase tensor2){
    return BaseConfigOp<BoolTensorBase, BoolTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 >= num2; });
}

pair<vector_bool, vector_i16> Ge(FloatTensorBase tensor1, DoubleTensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, DoubleTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1, tensor2,
    [](bool num1, bool num2) { return num1 >= num2; });
}

pair<vector_bool, vector_i16> Ge(Int32TensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<Int32TensorBase, Int64TensorBase, vector_bool, function<bool(int32_t, int64_t)>>(tensor1, tensor2,
        [](int32_t num1, int64_t num2) { return num1 >= num2; });
}

pair<vector_bool, vector_i16> Ge(FloatTensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, Int32TensorBase, vector_bool, function<bool(float, int32_t)>>(tensor1, tensor2,
        [](float num1, int32_t num2) { return num1 >= num2; });
}

pair<vector_bool, vector_i16> Ge(DoubleTensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, Int32TensorBase, vector_bool, function<bool(double, int32_t)>>(tensor1, tensor2,
        [](double num1, int32_t num2) { return num1 >= num2; });
}

pair<vector_bool, vector_i16> Ge(FloatTensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, Int64TensorBase, vector_bool, function<bool(float, int64_t)>>(tensor1, tensor2,
        [](float num1, int64_t num2) { return num1 >= num2; });
}

pair<vector_bool, vector_i16> Ge(DoubleTensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, Int64TensorBase, vector_bool, function<bool(double, int64_t)>>(tensor1, tensor2,
        [](double num1, int64_t num2) { return num1 >= num2; });
}

pair<vector_bool, vector_i16> Ge(DoubleTensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<DoubleTensorBase, FloatTensorBase, vector_bool, function<bool(double, float)>>(tensor1, tensor2,
        [](double num1, float num2) { return num1 >= num2; });
}

pair<vector_bool, vector_i16> Ge(Int32TensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<Int32TensorBase, FloatTensorBase, vector_bool, function<bool(int32_t, float)>>(tensor1, tensor2,
        [](int32_t num1, float num2) { return num1 >= num2; });
}

pair<vector_bool, vector_i16> Ge(Int64TensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<Int64TensorBase, FloatTensorBase, vector_bool, function<bool(int64_t, float)>>(tensor1, tensor2,
        [](int64_t num1, float num2) { return num1 >= num2; });
}

pair<vector_bool, vector_i16> Ge(Int32TensorBase tensor1, DoubleTensorBase tensor2) {
    return BaseConfigOp<Int32TensorBase, DoubleTensorBase, vector_bool, function<bool(int32_t, double)>>(tensor1, tensor2,
        [](int32_t num1, double num2) { return num1 >= num2; });
}

pair<vector_bool, vector_i16> Ge(Int64TensorBase tensor1, DoubleTensorBase tensor2) {
    return BaseConfigOp<Int64TensorBase, DoubleTensorBase, vector_bool, function<bool(int64_t, double)>>(tensor1, tensor2,
        [](int64_t num1, double num2) { return num1 >= num2; });
}

// -------------------Le---------------------
pair<vector_bool, vector_i16> Le(FloatTensorBase tensor1, FloatTensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, FloatTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 <= num2; });
}

pair<vector_bool, vector_i16> Le(DoubleTensorBase tensor1, DoubleTensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, DoubleTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 <= num2; });   
}

pair<vector_bool, vector_i16> Le(Int32TensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<Int32TensorBase, Int32TensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 <= num2; });
}

pair<vector_bool, vector_i16> Le(Int64TensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<Int64TensorBase, Int64TensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 <= num2; });
}

pair<vector_bool, vector_i16> Le(BoolTensorBase tensor1, BoolTensorBase tensor2){
    return BaseConfigOp<BoolTensorBase, BoolTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1,tensor2, 
    [](bool num1, bool num2) { return num1 <= num2; });
}

pair<vector_bool, vector_i16> Le(FloatTensorBase tensor1, DoubleTensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, DoubleTensorBase, vector_bool, function<bool(bool, bool)>>(tensor1, tensor2,
    [](bool num1, bool num2) { return num1 <= num2; });
}

pair<vector_bool, vector_i16> Le(Int32TensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<Int32TensorBase, Int64TensorBase, vector_bool, function<bool(int32_t, int64_t)>>(tensor1, tensor2,
        [](int32_t num1, int64_t num2) { return num1 <= num2; });
}

pair<vector_bool, vector_i16> Le(FloatTensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, Int32TensorBase, vector_bool, function<bool(float, int32_t)>>(tensor1, tensor2,
        [](float num1, int32_t num2) { return num1 <= num2; });
}

pair<vector_bool, vector_i16> Le(DoubleTensorBase tensor1, Int32TensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, Int32TensorBase, vector_bool, function<bool(double, int32_t)>>(tensor1, tensor2,
        [](double num1, int32_t num2) { return num1 <= num2; });
}

pair<vector_bool, vector_i16> Le(FloatTensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<FloatTensorBase, Int64TensorBase, vector_bool, function<bool(float, int64_t)>>(tensor1, tensor2,
        [](float num1, int64_t num2) { return num1 <= num2; });
}

pair<vector_bool, vector_i16> Le(DoubleTensorBase tensor1, Int64TensorBase tensor2){
    return BaseConfigOp<DoubleTensorBase, Int64TensorBase, vector_bool, function<bool(double, int64_t)>>(tensor1, tensor2,
        [](double num1, int64_t num2) { return num1 <= num2; });
}

pair<vector_bool, vector_i16> Le(DoubleTensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<DoubleTensorBase, FloatTensorBase, vector_bool, function<bool(double, float)>>(tensor1, tensor2,
        [](double num1, float num2) { return num1 <= num2; });
}

pair<vector_bool, vector_i16> Le(Int32TensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<Int32TensorBase, FloatTensorBase, vector_bool, function<bool(int32_t, float)>>(tensor1, tensor2,
        [](int32_t num1, float num2) { return num1 <= num2; });
}

pair<vector_bool, vector_i16> Le(Int64TensorBase tensor1, FloatTensorBase tensor2) {
    return BaseConfigOp<Int64TensorBase, FloatTensorBase, vector_bool, function<bool(int64_t, float)>>(tensor1, tensor2,
        [](int64_t num1, float num2) { return num1 <= num2; });
}

pair<vector_bool, vector_i16> Le(Int32TensorBase tensor1, DoubleTensorBase tensor2) {
    return BaseConfigOp<Int32TensorBase, DoubleTensorBase, vector_bool, function<bool(int32_t, double)>>(tensor1, tensor2,
        [](int32_t num1, double num2) { return num1 <= num2; });
}

pair<vector_bool, vector_i16> Le(Int64TensorBase tensor1, DoubleTensorBase tensor2) {
    return BaseConfigOp<Int64TensorBase, DoubleTensorBase, vector_bool, function<bool(int64_t, double)>>(tensor1, tensor2,
        [](int64_t num1, double num2) { return num1 <= num2; });
}

// -------------------Sum---------------------

pair<vector_f32, vector_i16> Sum(FloatTensorBase tensor, int32_t dim, bool keepdims) {
    return ReduceConfig<FloatTensorBase, vector_f32>(tensor, Ops::SUM, dim, keepdims);
}

pair<vector_f64, vector_i16> Sum(DoubleTensorBase tensor, int32_t dim, bool keepdims) {
    return ReduceConfig<DoubleTensorBase, vector_f64>(tensor, Ops::SUM, dim, keepdims);
}

pair<vector_f32, vector_i16> Sum(Int32TensorBase tensor, int32_t dim, bool keepdims) {
    return ReduceConfig<Int32TensorBase, vector_f32>(tensor, Ops::SUM, dim, keepdims);
}

pair<vector_f64, vector_i16> Sum(Int64TensorBase tensor, int32_t dim, bool keepdims) {
    return ReduceConfig<Int64TensorBase, vector_f64>(tensor, Ops::SUM, dim, keepdims);
}


// -------------------Mean---------------------

pair<vector_f32, vector_i16> Mean(FloatTensorBase tensor, int32_t dim, bool keepdims){
    return ReduceConfig<FloatTensorBase, vector_f32>(tensor, Ops::MEAN, dim, keepdims);
}
pair<vector_f64, vector_i16> Mean(DoubleTensorBase tensor, int32_t dim, bool keepdims) {
    return ReduceConfig<DoubleTensorBase, vector_f64>(tensor, Ops::MEAN, dim, keepdims);
}
pair<vector_f32, vector_i16> Mean(Int32TensorBase tensor, int32_t dim, bool keepdims){
    return ReduceConfig<Int32TensorBase, vector_f32>(tensor, Ops::MEAN, dim, keepdims);
}
pair<vector_f64, vector_i16> Mean(Int64TensorBase tensor, int32_t dim, bool keepdims){
    return ReduceConfig<Int64TensorBase, vector_f64>(tensor, Ops::MEAN, dim, keepdims);
}


// -------------------Median---------------------

pair<vector_f32, vector_i16> Median(FloatTensorBase tensor, int32_t dim, bool keepdims){
    return ReduceConfig<FloatTensorBase, vector_f32>(tensor, Ops::MEDIAN, dim, keepdims);
}
pair<vector_f64, vector_i16> Median(DoubleTensorBase tensor, int32_t dim, bool keepdims) {
    return ReduceConfig<DoubleTensorBase, vector_f64>(tensor, Ops::MEDIAN, dim, keepdims);
}
pair<vector_f32, vector_i16> Median(Int32TensorBase tensor, int32_t dim, bool keepdims){
    return ReduceConfig<Int32TensorBase, vector_f32>(tensor, Ops::MEDIAN, dim, keepdims);
}
pair<vector_f64, vector_i16> Median(Int64TensorBase tensor, int32_t dim, bool keepdims){
    return ReduceConfig<Int64TensorBase, vector_f64>(tensor, Ops::MEDIAN, dim, keepdims);
}


// -------------------Min---------------------

pair<vector_f32, vector_i16> Min(FloatTensorBase tensor, int32_t dim, bool keepdims){
    return ReduceConfig<FloatTensorBase, vector_f32>(tensor, Ops::MIN, dim, keepdims);
}
pair<vector_f64, vector_i16> Min(DoubleTensorBase tensor, int32_t dim, bool keepdims) {
    return ReduceConfig<DoubleTensorBase, vector_f64>(tensor, Ops::MIN, dim, keepdims);
}
pair<vector_f32, vector_i16> Min(Int32TensorBase tensor, int32_t dim, bool keepdims){
    return ReduceConfig<Int32TensorBase, vector_f32>(tensor, Ops::MIN, dim, keepdims);
}
pair<vector_f64, vector_i16> Min(Int64TensorBase tensor, int32_t dim, bool keepdims){
    return ReduceConfig<Int64TensorBase, vector_f64>(tensor, Ops::MIN, dim, keepdims);
}


// -------------------Max---------------------

pair<vector_f32, vector_i16> Max(FloatTensorBase tensor, int32_t dim, bool keepdims){
    return ReduceConfig<FloatTensorBase, vector_f32>(tensor, Ops::MAX, dim, keepdims);
}
pair<vector_f64, vector_i16> Max(DoubleTensorBase tensor, int32_t dim, bool keepdims) {
    return ReduceConfig<DoubleTensorBase, vector_f64>(tensor, Ops::MAX, dim, keepdims);
}
pair<vector_f32, vector_i16> Max(Int32TensorBase tensor, int32_t dim, bool keepdims){
    return ReduceConfig<Int32TensorBase, vector_f32>(tensor, Ops::MAX, dim, keepdims);
}
pair<vector_f64, vector_i16> Max(Int64TensorBase tensor, int32_t dim, bool keepdims){
    return ReduceConfig<Int64TensorBase, vector_f64>(tensor, Ops::MAX, dim, keepdims);
}