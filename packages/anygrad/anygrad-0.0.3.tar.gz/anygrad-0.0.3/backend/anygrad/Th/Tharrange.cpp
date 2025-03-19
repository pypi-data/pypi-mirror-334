#include <vector>
#include <utility>
#include <limits>
#include <algorithm>

#include "../include/ThTypes.hpp"
#include "../include/Th.hpp"

using namespace std;

template <typename U, typename V>
pair<V, vector_i16> ViewConfig(U tensor, vector_i16 new_shape_input){
    
    int neg_indx = 0;
    int32_t new_dim = 1;
    //this one is handle the one negative index
    for (auto d : new_shape_input) {if (d == -1) neg_indx++; else new_dim *= d;}
    
    vector_i16 new_shape;
    new_shape.resize(new_shape_input.size());
    if (neg_indx == 1) {
        int new_size = tensor.size / new_dim;
        for (size_t i = 0; i < new_shape_input.size(); i++)
            new_shape[i] = (new_shape_input[i] == -1) ? new_size : new_shape_input[i];
    } else 
        new_shape = new_shape_input;
    
    return {tensor.data, new_shape};
}

pair<vector_f32, vector_i16> View(FloatTensorBase tensor, vector_i16 rearrenge_view){
    return ViewConfig<FloatTensorBase, vector_f32>(tensor, rearrenge_view);
}

pair<vector_f64, vector_i16> View(DoubleTensorBase tensor, vector_i16 rearrenge_view){
    return ViewConfig<DoubleTensorBase, vector_f64>(tensor, rearrenge_view);
}

pair<vector_i32, vector_i16> View(Int32TensorBase tensor, vector_i16 rearrenge_view){
    return ViewConfig<Int32TensorBase, vector_i32>(tensor, rearrenge_view);
}

pair<vector_i64, vector_i16> View(Int64TensorBase tensor, vector_i16 rearrenge_view){
    return ViewConfig<Int64TensorBase, vector_i64>(tensor, rearrenge_view);
}

pair<vector_bool, vector_i16> View(BoolTensorBase tensor, vector_i16 rearrenge_view){
    return ViewConfig<BoolTensorBase, vector_bool>(tensor, rearrenge_view);
}
