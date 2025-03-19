#ifndef GENERATOR_HPP
#define GENERATOR_HPP

#include <vector>
#include <utility>
#include <string>
#include <random>

#include "ThTypes.hpp"
#include "Th.hpp"

using namespace std;

class Generator{
    public:
        int32_t _state;
        Generator(int32_t seed = random_device{}()) : engine(seed){}

        void manual_seed(int32_t seed){
            engine.seed(seed);
        }

        int32_t randint(int32_t start, int32_t end){
            uniform_int_distribution<int> dist(start, end);
            return dist(engine);
        }

        double randfloat(double start = 0.0, double end = 1.0){
            uniform_real_distribution<double> dist(start, end);
            return dist(engine);
        }

    private:
        mt19937 engine;

};

#endif