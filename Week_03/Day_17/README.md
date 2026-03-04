# Day 17 - First PyTorch Project

## What I Built
XOR problem solved with PyTorch. Same problem as Day 15/16
but using PyTorch's nn.Module instead of raw NumPy.

## What I Learned
- nn.Module = base class for all PyTorch networks
- nn.Linear = weight + bias handled automatically
- loss.backward() = entire backprop in one line
- optimizer.step() = all weight updates in one line
- torch.no_grad() = disable gradient tracking for inference
- Capital X vs lowercase x — one letter bug crashes everything

## Comparison
NumPy (Day 15): ~100 lines, manual everything
PyTorch (Day 17): ~50 lines, framework handles backprop

## Result
4/4 XOR predictions correct
Total parameters: 193
Loss: 0.70 → ~0.00

## Tech Used
Python, PyTorch