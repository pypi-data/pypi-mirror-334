from typing import NewType
from anygrad.tensor.base import tensor_c as C
from collections.abc import Sequence
from collections import Counter, deque
from functools import reduce
from operator import mul


float32 = NewType("float32", C.float32)
float32.__module__ = "anygrad"
float64 = NewType("float64", C.float64)
float64.__module__ = "anygrad"
int32 = NewType("int32", C.int32)
int32.__module__ = "anygrad"
int64 = NewType("int64", C.int64)
int64.__module__ = "anygrad"
bool = NewType("bool", C.bool)
bool.__module__ = "anygrad"

def convert_tensor(data, conv_type):
    if not isinstance(data, list):
        return conv_type(data)
    return [convert_tensor(ele, conv_type) for ele in data]

def valid_data_type(data):
    flat = flat_list(data) if isinstance(data, list) else [data]
    counter = Counter(type(x) for x in flat)
    return max(counter, key=counter.get)

def flat_list(data):
    if not isinstance(data, list):
        return data
    result = []
    queue = deque([data])
    while queue:
        current = queue.popleft()
        if isinstance(current, list):
            queue.extend(current)
        else:
            result.append(current)
    return result

def cal_shape(data):
    shape = []
    while isinstance(data, Sequence) and not isinstance(data, (str, bytes)):
        if not data:
            shape.append(0)
            break
        if isinstance(data[0], Sequence):
            expected_len = len(data[0])
            if any(len(item) != expected_len for item in data):
                raise ValueError("Not all lists have the same length in your data")
        shape.append(len(data))
        data = data[0]
    return tuple(shape)

def reshape(data, shape):
    
    if reduce(mul, shape) != len(data):
        raise ValueError(f"Given {shape} shape is not compatable with data")
    
    if len(shape) == 1:
        return data

    n = reduce(mul, shape[1:])
    return [reshape(data[i*n: (i + 1)*n], shape[1:]) for i in range(len(data) // n)]


def round_list(data, round_factor=4):
    if isinstance(data, list):
        return [round_list(item, round_factor) for item in data]
    return round(data, round_factor)


