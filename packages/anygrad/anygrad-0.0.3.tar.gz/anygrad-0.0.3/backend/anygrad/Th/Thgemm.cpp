#include <vector>
#include <utility>
#include <algorithm>

#include "../include/Th.hpp"
#include "../include/ThTypes.hpp"

using namespace std;



//function that check two mat is able to multiply or not?
bool is_matmul_broadcast(vector_i16 shape1, vector_i16 shape2, int32_t dim1, int32_t dim2) {
    int max_dim = max(dim1, dim2);
    if (dim2 == 1) { //for 2d? 
        if (shape1[dim1 - 1] != shape2[0]) // directly checking the shape
            return false; 
    } else if (shape1[dim1 - 1] != shape2[dim2 - 2]) { // what this dose? 
        return false;
    }
    // (1, 2, 3, 4) && (2, 2, 4, 3) # relate to this example this will throws the ture
    for (int i = 0; i < max_dim - 2; i++) { // skiping the last two dims and check the other dims that are same or 1.
        int new_dim1 = (i >= dim1 - 2) ? 1 : shape1[dim1 - 3 - i]; // this is allow to handle this types of shapes (1, 2, 3) and (3, 2) which are also broadcasteble
        int new_dim2 = (i >= dim2 - 2) ? 1 : shape2[dim2 - 3 - i]; // "

        if (new_dim1 != 1 && new_dim2 != 1 && new_dim1 != new_dim2) // now let check if that new selected dim is 1 or same.
            return false;
    }
    return true;
}

//caculate the new shape that are used for the new and matmul
vector_i16 matmul_broadcast_shape(vector_i16 shape1, vector_i16 shape2, int32_t dim1, int32_t dim2) {
    int max_dim = max(dim1, dim2);
    vector_i16 shape3(max_dim); 

    for (int i = 0; i < max_dim - 2; i++) { // skiping the last two dims and check that other dims are same or not 
        int new_dim1 = (i >= dim1 - 2) ? 1 : shape1[dim1 - 3 - i]; // if one shape is smaller then the other then we use the 1 because of the broadcasting
        int new_dim2 = (i >= dim2 - 2) ? 1 : shape2[dim2 - 3 - i]; // "
        if (max_dim - 3 - i >= 0) {  // applying the shape for broadcase like in example we perfrom this from this 
                                    // (1) && (2) max(1, 2) -> (2, -, -, -); i = 0
                                    // (2) && (2) max(2, 2) -> (2, 2, _, _); i = 1
            shape3[max_dim - 3 - i] = max(new_dim1, new_dim2);
        }
    }
    //set the shape manually for second last dim and last dim
    shape3[max_dim - 2] = shape1[dim1 - 2]; // second last dim 
                                            // (3) -> (2, 2, 3, _)
    shape3[max_dim - 1] = (dim2 == 1) ? 1 : shape2[dim2 - 1]; // last dim
                                                              // (3) -> (2, 2, 3, 3)
    return shape3;
}

//do the 2D matmul oprations for each batch 
//example : 
// [[2, 3], [4, 5]] && [[3, 6], [1, 7]] # just for visul
// use this as a linear memory 
// [2, 3, 4, 5] && [3, 6, 1, 7]
// ans is shape is must (2, 2) out I_shape: 2, J_shape: 2, K_shape: 2
// other example shape1 (1, 3) and shape2 (3, 5) the the ans_shape is must (1, 5) os the I_shape: 1(comes from ans), J_shape: 5(comes from ans) and K_shape: 3(comes from the shape1) 
template <typename U>
U matmul2d(U& data1, U& data2, int32_t I_shape, int32_t K_shape, int32_t J_shape) {
    const int32_t block_size = 16; // block_size which just cache the memory of the CPU if those tensors are too big
    U ans_data(I_shape * J_shape, 0); // so the ans shape is in our case is like this (2 * 2) fills with 0 (_, _, _, _)

    // so ii[0, 2) && jj[0, 2) && kk[0, 2)
    for (int ii = 0; ii < I_shape; ii += block_size) { // getting the first block first row
        for (int jj = 0; jj < J_shape; jj += block_size) { // getting the first block second row
            for (int kk = 0; kk < K_shape; kk += block_size) { // this shape is like set the value for ans block
                // so i, j, k is [0, 2)
                for (int i = ii; i < min(ii + block_size, I_shape); ++i) { // go inside the first block also checking is that which one is bigger (I_shape or I_shape + block_size)
                    for (int j = jj; j < min(jj + block_size, J_shape); ++j) {
                        // Use the element type of U to avoid precision issues in accumulation
                        using value_type = typename U::value_type;
                        value_type sum = 0;
                        for (int k = kk; k < min(kk + block_size, K_shape); ++k) {
                            // i = 0 j = 0 k = 0 we get the index (0, 0) -> 2 and 3; sum = 6 sum += 6
                            // i = 0 j = 0 k = 1 we get the index (1, 2) -> 3 and 1; sum = 3 sum += 9
                            // like wise ops are happend
                            sum += data1[i * K_shape + k] * data2[k * J_shape + j]; // doing the oprations of matmul and updating the reduce sum
                        }
                        // i = 0 j = 0 -> 0; (9, _, _, _)
                        ans_data[i * J_shape + j] += sum; // adding to the ans_data 
                    }
                }
            }
        }
    }
    return ans_data;
}

// we use this 2D matmul and apply it for the Nd matmul that help to reduce the complexity of the code
// example:
// [[2, 3], [4, 5]] && [[3, 6], [1, 7]] # just for visul
// use this as a linear memory 
// [2, 3, 4, 5] && [3, 6, 1, 7]
template <typename T, typename U>
pair<U, vector_i16> matmulNd(T& tensor1, T& tensor2) {
    vector_i16 ans_shape = matmul_broadcast_shape(tensor1.shape, tensor2.shape, tensor1.ndim, tensor2.ndim); // first we get the ans_shape for broadcasting
    // ans_shape = (2, 2)
    int32_t ans_dim = ans_shape.size(); // caculate the dim of the new shape
    // ans_dim = 2
    int32_t size = calculate_size(ans_shape, ans_dim); // caculate the size(numel)
    // size = 4
    int32_t max_dim = max(tensor1.ndim, tensor2.ndim);// get the max dim
    // max_dim = 2

    vector_i16 result_stride1 = broadcast_stride(tensor1.shape, tensor1.stride, tensor1.ndim, max_dim); // caculate the broadcast shape
    // result_stride1 = (2, 2)
    vector_i16 result_stride2 = broadcast_stride(tensor2.shape, tensor2.stride, tensor2.ndim, max_dim);
    // result_stride2 = (2, 2)

    int32_t batch_size = calculate_size(ans_shape, ans_dim - 2);// getthing size up to the batch
    // batch_size = 4, from the ans_shape = (2, 2)
    
    U result_data(size, 0); // creating the linear memory of the result_data
    
    // as explain in matmul2d why we need this
    int32_t row_size = ans_shape[ans_dim - 2]; // extract the shape for first mat 
    // row_size = 2 row
    int32_t col_size = ans_shape[ans_dim - 1]; // extrect the shape for second mat
    // col_size = 2 col
    int32_t inner_size = tensor1.shape[tensor1.ndim - 1]; // this shape is used in ans mat fillinng 
    // inner_size = 2 inner shape

    //batch_strdie
    vector_i16 batch_stride = calculate_stride(ans_shape, batch_size);

    for (int b = 0; b < batch_size; b++) { 
        U batch_data1(row_size * inner_size); // make the sample batch_data size of (row_size * inner_size) and (inner_size * col_size)
        U batch_data2(inner_size * col_size); 
        
        // filling the data for batch1
        for (int i = 0; i < row_size; i++) {
            for (int k = 0; k < inner_size; k++) {
                size_t offset1 = 0;
                for (int d = 0; d < max_dim - 2; d++) { // go for each new batch to fill the data
                    int batch_idx = (b / batch_stride[d]) % ans_shape[d]; // get the new batch_index
                    // b = 0, d = 0, batch_idx = (0 / batch_stride[0]) % ans_shape[0]
                    // batch_idx = 0 % 2 = 0
                    offset1 += batch_idx * result_stride1[d]; // update the offset in terms of the result stride
                    // offset1 = 0
                }
                offset1 += i * tensor1.stride[tensor1.ndim - 2] + k * tensor1.stride[tensor1.ndim - 1]; // update the offset in terms of the stride
                // i = 0, tensor1.stride = (2, 1), tensor1.ndim = 2, 
                // offset1 = 0 * 2 + 0 * 1 = 0
                // offset1 = 0 
                batch_data1[i * inner_size + k] = tensor1.data[offset1]; // update the data safely
                // i * inner_size + k = 0 * 2 + 0 = 0 
                // batch_data1[0] = tensor1.data[0]
            }
        }
        
        //filling the data for batch2
        // same as for row_size
        for (int k = 0; k < inner_size; k++) {
            for (int j = 0; j < col_size; j++) {
                size_t offset2 = 0;
                for (int d = 0; d < max_dim - 2; d++) {
                    int batch_idx = (b / batch_stride[d]) % ans_shape[d];
                    offset2 += batch_idx * result_stride2[d];
                }
                offset2 += k * tensor2.stride[tensor2.ndim - 2] + j * tensor2.stride[tensor2.ndim - 1];
                batch_data2[k * col_size + j] = tensor2.data[offset2];
            }
        }
        
        U batch_result = matmul2d(batch_data1, batch_data2, row_size, inner_size, col_size); // get the matmul2d of the first and second batch
        
        copy(batch_result.begin(), batch_result.end(), result_data.begin() + b * row_size * col_size); // copy the hole data into the result data
    }

    vector_i16().swap(result_stride1);
    vector_i16().swap(result_stride2);
    vector_i16().swap(batch_stride);

    return {result_data, ans_shape};
}

template <typename T>
T transpose2d(T& data1, int32_t rows, int32_t cols) {
    T ans_data(rows * cols);
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            ans_data[i + j * rows] = data1[i * cols + j];
        }
    }
    return ans_data;
}

template <typename T, typename U>
pair<U, vector_i16> transposeNd(T tensor1, int32_t dim0, int32_t dim1) {
    vector_i16 shape = tensor1.shape;
    swap(shape[dim0], shape[dim1]);
    
    U result_data(tensor1.size);
    
    int32_t dim0_size = tensor1.shape[dim0];
    int32_t dim1_size = tensor1.shape[dim1];
    int32_t block_size = dim0_size * dim1_size;
    
    int32_t outer_size = calculate_size(tensor1.shape, min(dim0, dim1));
    
    int32_t inner_size = 1;
    for (int i = max(dim0, dim1) + 1; i < tensor1.ndim; i++) {
        inner_size *= tensor1.shape[i];
    }
    
    for (int i = 0; i < outer_size; i++) {
        for (int j = 0; j < inner_size; j++) {
            int32_t offset = i * block_size * inner_size + j * block_size;
            U block(tensor1.data.begin() + offset, tensor1.data.begin() + offset + block_size);

            U transposed = transpose2d(block, dim0_size, dim1_size);
            copy(transposed.begin(), transposed.end(), result_data.begin() + offset);
        }
    }
    
    return {result_data, shape};
}

pair<vector_f32, vector_i16> Matmul(FloatTensorBase tensor1, FloatTensorBase tensor2){
    return matmulNd<FloatTensorBase, vector_f32>(tensor1, tensor2);
}

pair<vector_f64, vector_i16> Matmul(DoubleTensorBase tensor1, DoubleTensorBase tensor2){
    return matmulNd<DoubleTensorBase, vector_f64>(tensor1, tensor2);
}

pair<vector_i32, vector_i16> Matmul(Int32TensorBase tensor1, Int32TensorBase tensor2){
    return matmulNd<Int32TensorBase, vector_i32>(tensor1, tensor2);
}

pair<vector_i64, vector_i16> Matmul(Int64TensorBase tensor1, Int64TensorBase tensor2){
    return matmulNd<Int64TensorBase, vector_i64>(tensor1, tensor2);
}

pair<vector_f32, vector_i16> Trans(FloatTensorBase tensor, int32_t dim0, int32_t dim1){
    return transposeNd<FloatTensorBase, vector_f32>(tensor, dim0, dim1);
}

pair<vector_f64, vector_i16> Trans(DoubleTensorBase tenosr, int32_t dim0, int32_t dim1){
    return transposeNd<DoubleTensorBase, vector_f64>(tenosr, dim0, dim1);
}

pair<vector_i32, vector_i16> Trans(Int32TensorBase tensor, int32_t dim0, int32_t dim1){
    return transposeNd<Int32TensorBase, vector_i32>(tensor, dim0, dim1);
}

pair<vector_i64, vector_i16> Trans(Int64TensorBase tensor, int32_t dim0, int32_t dim1){
    return transposeNd<Int64TensorBase, vector_i64>(tensor, dim0, dim1);
}

pair<vector_bool, vector_i16> Trans(BoolTensorBase tensor, int32_t dim0, int32_t dim1){
    return transposeNd<BoolTensorBase, vector_bool>(tensor, dim0, dim1);
}