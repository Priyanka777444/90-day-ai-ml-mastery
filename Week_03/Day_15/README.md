# Day 15 - Neural Network From Scratch

## What I Built
2-layer neural network trained on XOR problem using 
backpropagation and gradient descent. No PyTorch, no TensorFlow. 
Pure NumPy.

## What I Learned
- Forward pass: input → hidden layer (ReLU) → output (Sigmoid)
- Backward pass: gradients flow backwards through each layer
- NaN = exploding gradients → fix with He initialization + lower lr
- He initialization: np.sqrt(2/input_size) for ReLU networks
- XOR is not linearly separable → needs hidden layers → needs neural network
- Logistic regression draws one line, NN creates non-linear boundary

## Result
[0,0] → Expected: 0 | Predicted: 0.0011 ✅
[0,1] → Expected: 1 | Predicted: 0.9995 ✅
[1,0] → Expected: 1 | Predicted: 0.9996 ✅
[1,1] → Expected: 0 | Predicted: 0.0003 ✅

4/4 Perfect predictions.

## Tech Used
Python, NumPy, Matplotlib

## Key Concepts
ReLU: max(0, x) → kills negative values
Sigmoid: 1/(1+e^-x) → squishes output to 0-1
He Init: weights * sqrt(2/n) → prevents NaN in deep networks