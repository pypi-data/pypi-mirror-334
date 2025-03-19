#include <vector>
#include <iostream>

#include "../include/Th.hpp"

using namespace std;


vector_i16 calculate_stride(vector_i16 shape, int32_t ndim){
    vector_i16 stride(ndim); 
    stride[ndim - 1] = 1;
    for(int i = ndim - 2; i >= 0; i--){
        stride[i] = stride[i+1] * shape[i+1];
    }
    return stride;
}

int32_t calculate_size(vector_i16 shape, int32_t ndim){
    int32_t size = 1;
    for(int32_t i = 0; i < ndim; i++)
        size *= shape[i];
    return size;
}

vector_i16 broadcast_stride(vector_i16 shape, vector_i16 stride, int32_t dim, int32_t max_dim){
    vector_i16 result_stride(max_dim); 
    for(int i = 0; i < max_dim; i++){
        int dim_a = (i >= dim) ? 1 : shape[dim - 1 - i];
        result_stride[max_dim - 1 - i] = (dim_a == 1) ? 0 : stride[dim - 1 - i];
    }
    return result_stride;
}

vector_i16 broadcast_shape(vector_i16 shape1, vector_i16 shape2, int32_t dim1, int32_t dim2, int32_t max_dim){
    vector_i16 result_shape(max_dim, 0);
    for(int i = 0; i < max_dim; i++){
        int32_t dim_a = (i >= dim1) ? 1 : shape1[dim1 - 1 - i];
        int32_t dim_b = (i >= dim2) ? 1 : shape2[dim2 - 1 - i];
        result_shape[max_dim - 1 - i] = (dim_a > dim_b) ? dim_a : dim_b;
    }
    return result_shape;
}

bool isbroadcast(vector_i16 shape1, vector_i16 shape2, int dim1, int dim2) {
    int max_dim = max(dim1, dim2);
    for (int i = 0; i < max_dim; i++) {
        int dim_a = (i >= dim1) ? 1 : shape1[dim1 - 1 - i];
        int dim_b = (i >= dim2) ? 1 : shape2[dim2 - 1 - i];
        if (dim_a != 1 && dim_b != 1 && dim_a != dim_b) {
            return false;
        }
    }
    return true; 
}

void update_offset(int32_t *offset1, int32_t *offset2, int32_t *n_idx, int32_t max_dim, vector_i16 stride, vector_i16 resut_stride1, vector_i16 resut_stride2){
    for (int i = 0; i < max_dim; i++){
        int stride_idx = *n_idx / stride[i];
        *n_idx %= stride[i];
        *offset1 += stride_idx * resut_stride1[i];
        *offset2 += stride_idx * resut_stride2[i];
    }
}

bool is_sum_allow(int32_t dim_to_sum, int32_t tensor_dim){
    if (dim_to_sum == -1)
        return true;
    if (dim_to_sum < -1 || dim_to_sum >= tensor_dim)
        return false;
    return true;
}


bool is_view_allow(vector_i16 new_view, int32_t size){
    int neg_indx = 0;
    int64_t new_dim = 1;
    for (auto d : new_view) {if (d == -1) neg_indx++; else new_dim *= d;}

    if (neg_indx > 1)
        return false;
    if (neg_indx == 1) {
        if (size % new_dim != 0)
            return false;
    } else {
        if (new_dim != size)
            return false;
    }
    return true;
}