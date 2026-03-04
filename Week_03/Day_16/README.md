# Day 16 - Backpropagation + Deep Network

## What I Built
3-layer neural network with gradient flow visualization.
Solved XOR and observed vanishing gradients across layers.

## What I Learned
- Chain rule applied backwards = backpropagation
- Each weight gets blamed proportionally for the error
- Vanishing gradients: Layer 1 gets weaker signal than Layer 3
- Deeper networks = harder to train = need ResNets/BatchNorm/Adam
- He initialization prevents NaN in deep ReLU networks

## Result
4/4 XOR predictions correct
Gradient flow visualized across all 3 layers

## Tech Used
Python, NumPy, Matplotlib

## Key Concept
Backprop = Chain Rule backwards
dLoss/dW1 = dLoss/dW3 × dW3/dW2 × dW2/dW1