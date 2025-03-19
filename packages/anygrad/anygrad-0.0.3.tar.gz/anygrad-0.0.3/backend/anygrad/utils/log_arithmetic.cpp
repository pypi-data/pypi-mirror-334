#include <vector>
#include <utility>

#include "../include/ThTypes.hpp"
#include "../include/Th.hpp"



using namespace std;

template <typename T, typename U, typename Op>
pair<U, vector_i16> LogConfig(T tensor1, Op op){
    U result_data(tensor1.size);
    for(int32_t i = 0; i < tensor1.size; i++){
        result_data[i] = op(tensor1.data[i]);
    }
    return {result_data, tensor1.shape};
}

pair<vector_f32, vector_i16> LogFloat32(FloatTensorBase tensor1){
    return LogConfig<FloatTensorBase, vector_f32, function<float(float)>> (tensor1, 
    [](float num) {return log(num);});
}

pair<vector_f64, vector_i16> LogFloat64(DoubleTensorBase tensor1){
    return LogConfig<DoubleTensorBase, vector_f64, function<double(double)>> (tensor1, 
    [](double num) {return log(num);});
}

pair<vector_f32, vector_i16> LogInt32(Int32TensorBase tensor1){
    return LogConfig<Int32TensorBase, vector_f32, function<float(float)>> (tensor1, 
    [](float num) {return log(static_cast<float>(num));});
}

pair<vector_f64, vector_i16> LogInt64(Int64TensorBase tensor1){
    return LogConfig<Int64TensorBase, vector_f64, function<double(double)>> (tensor1, 
    [](double num) {return log(static_cast<double>(num));});
}

pair<vector_f32, vector_i16> Log10Int32(Int32TensorBase tensor1){
    return LogConfig<Int32TensorBase, vector_f32, function<float(float)>> (tensor1, 
        [](float num) { return log10(static_cast<float>(num)); });
}

pair<vector_f64, vector_i16> Log10Int64(Int64TensorBase tensor1){
    return LogConfig<Int64TensorBase, vector_f64, function<double(double)>> (tensor1, 
        [](double num) { return log10(static_cast<double>(num)); });
}

pair<vector_f32, vector_i16> Log2Int32(Int32TensorBase tensor1){
    return LogConfig<Int32TensorBase, vector_f32, function<float(float)>> (tensor1, 
        [](float num) { return static_cast<float>(log2(static_cast<double>(num))); });
}

pair<vector_f64, vector_i16> Log2Int64(Int64TensorBase tensor1){
    return LogConfig<Int64TensorBase, vector_f64, function<double(double)>> (tensor1, 
        [](double num) { return static_cast<double>(log2(static_cast<double>(num))); });
}

pair<vector_f32, vector_i16> ExpFloat32(FloatTensorBase tensor1){
    return LogConfig<FloatTensorBase, vector_f32, function<float(float)>> (tensor1, 
    [](float num) {return exp(num);});
}

pair<vector_f64, vector_i16> ExpFloat64(DoubleTensorBase tensor1){
    return LogConfig<DoubleTensorBase, vector_f64, function<double(double)>> (tensor1, 
    [](double num) {return exp(num);});
}

pair<vector_f32, vector_i16> ExpInt32(Int32TensorBase tensor1){
    return LogConfig<Int32TensorBase, vector_f32, function<float(float)>> (tensor1, 
        [](float num) { return static_cast<float>(exp(static_cast<double>(num))); });
}

pair<vector_f64, vector_i16> ExpInt64(Int64TensorBase tensor1){
    return LogConfig<Int64TensorBase, vector_f64, function<double(double)>> (tensor1, 
        [](double num) { return static_cast<double>(exp(static_cast<double>(num))); });
}

pair<vector_f32, vector_i16> Exp2Float32(FloatTensorBase tensor1){
    return LogConfig<FloatTensorBase, vector_f32, function<float(float)>> (tensor1, 
        [](float num) { return (exp2((num))); });
}

pair<vector_f64, vector_i16> Exp2Float64(DoubleTensorBase tensor1){
    return LogConfig<DoubleTensorBase, vector_f64, function<double(double)>> (tensor1, 
        [](double num) { return (exp2((num))); });
}

pair<vector_f32, vector_i16> Exp2Int32(Int32TensorBase tensor1){
    return LogConfig<Int32TensorBase, vector_f32, function<float(float)>> (tensor1, 
        [](float num) { return static_cast<float>(exp2(static_cast<double>(num))); });
}

pair<vector_f64, vector_i16> Exp2Int64(Int64TensorBase tensor1){
    return LogConfig<Int64TensorBase, vector_f64, function<double(double)>> (tensor1, 
        [](double num) { return static_cast<double>(exp2(static_cast<double>(num))); });
}

pair<vector_f32, vector_i16> Log10Float32(FloatTensorBase tensor1){
    return LogConfig<FloatTensorBase, vector_f32, function<float(float)>> (tensor1, 
    [](float num) {return log10(num);});
}

pair<vector_f64, vector_i16> Log10Float64(DoubleTensorBase tensor1){
    return LogConfig<DoubleTensorBase, vector_f64, function<double(double)>> (tensor1, 
    [](double num) {return log10(num);});
}

pair<vector_f32, vector_i16> Log2Float32(FloatTensorBase tensor1){
    return LogConfig<FloatTensorBase, vector_f32, function<float(float)>> (tensor1, 
    [](float num) {return log2(num);});
}

pair<vector_f64, vector_i16> Log2Float64(DoubleTensorBase tensor1){
    return LogConfig<DoubleTensorBase, vector_f64, function<double(double)>> (tensor1, 
    [](double num) {return log2(num);});
}
