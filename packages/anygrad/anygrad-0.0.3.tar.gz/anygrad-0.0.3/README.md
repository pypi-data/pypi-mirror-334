<div align="center">
  
# 🚂 AnyGrad: Flexible Engine for Tensor and Neural Network.

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)  [![PyPI Version](https://img.shields.io/pypi/v/anygrad?color=yellow&logo=pypi)](https://pypi.org/project/anygrad/)  


</div>

## Overview
AnyGrad is a simple tensor library that makes it easy to perform forward and backward passes. It uses a high-performance C++ backend together with a user-friendly Python frontend. You can change the backend easily and simply.

> Note: currently version `0.0.1` does not support any engine. 
But in the future, the integrations of engines like `numpy`, `pytorch` etc. will come and you can use them for anything from Tensor operation to high-level transformer training. 

## Installation
Install the library from PyPI:
```bash
pip install anygrad
```

If you'd like to work on the code:
```bash
git clone https://github.com/Ruhaan838/AnyGrad.git
./setup.sh
```

## Getting Started
### Creating a Tensor
Create tensors by importing the library and instantiating `Tensor`. By default, gradients are not tracked unless you enable them:
```python
import anygrad

# A tensor that does not calculate gradients
a = anygrad.Tensor([1, 2, 3])  

# A tensor with gradient tracking enabled
b = anygrad.Tensor([2, 3, 4], requires_grad=True)  

# A tensor with a specific data type (float64)
c = anygrad.Tensor([2, 3, 4], dtype=anygrad.float64)
```
> Other datatypes:<br>
anygrad.int32 <br>
anygrad.int64 <br>
anygrad.bool <br>

### Arithmetic Operations
#### Element-wise Operations
Perform calculations on tensors element by element:
```python
d = a + b         # addition
d = a * d         # multiplication
d = d / 10        # division
e = d - 10        # subtraction
```

#### Matrix Multiplication
You can multiply matrices in two ways:
```python
# Using the @ operator:
a = anygrad.ones((1, 2, 3), requires_grad=True)
b = anygrad.ones((2, 3, 4), requires_grad=True)
c = a @ b         # tensor of shape (2, 2, 4)

# Or using the function:
c = anygrad.matmul(a, b)
```

### Gradient Calculation
AnyGrad automatically computes gradients, which you can access after running the backward pass:
```python
a = anygrad.Tensor([1, 2, 3], requires_grad=True)
b = anygrad.Tensor([2, 3, 4], requires_grad=True)
c = a * b 
result = c.sum()
result.backward()

print(a.grad)
print(b.grad)
```

## Contributing
Contributions are welcome! Whether you want to improve performance or enhance the documentation, please open an issue or submit a pull request.

## License
This project is licensed under the terms outlined in the [LICENSE](LICENSE) file.