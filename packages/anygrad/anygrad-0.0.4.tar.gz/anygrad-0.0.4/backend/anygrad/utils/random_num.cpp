#include <vector>
#include <utility>
#include <string>
#include <random>

#include "../include/ThTypes.hpp"
#include "../include/Th.hpp"
#include "../include/generator.hpp"

using namespace std;



template <typename U, typename T>
pair<U, vector_i16> randConfig(vector_i16 shape, Generator* generator){
    U result_data;

    //local engine
    static mt19937 global_engine(random_device{}());
    static uniform_real_distribution<T> gloabal_dist(0.0, 1.0);

    int32_t size = calculate_size(shape, shape.size());
    result_data.resize(size, 0); //initalize the data
    for (int32_t i = 0; i < size; i++){
        if(generator)
            result_data[i] = generator->randfloat();
        else
            result_data[i] = gloabal_dist(global_engine);
    }

    return {result_data, shape};
}

template <typename U, typename T>
pair<U, vector_i16> randintConfig(vector_i16 shape, int32_t low, int32_t high, Generator* generator){
    U result_data;

    static mt19937 global_engine(random_device{}());
    static uniform_int_distribution<T> gloabal_dist(low, high);

    int32_t size = calculate_size(shape, shape.size());
    result_data.resize(size, 0);
    for (int32_t i = 0; i < size; i++){
        if(generator)
            result_data[i] = generator->randint(low, high);
        else
            result_data[i] = gloabal_dist(global_engine);
    }

    return {result_data, shape};
}

pair<vector_f32, vector_i16> randFloat32(vector_i16 shape, Generator *generator){
    return randConfig<vector_f32, float>(shape, generator);
}
pair<vector_f64, vector_i16> randFloat64(vector_i16 shape, Generator *generator){
    return randConfig<vector_f64, double>(shape, generator);
}

pair<vector_i32, vector_i16> randintInt32(vector_i16 shape, int32_t low, int32_t high, Generator *generator){
    return randintConfig<vector_i32, int32_t>(shape, low, high, generator);
}

pair<vector_i64, vector_i16> randintInt64(vector_i16 shape, int32_t low, int32_t high, Generator *generator){
    return randintConfig<vector_i64, int32_t>(shape, low, high, generator);
}