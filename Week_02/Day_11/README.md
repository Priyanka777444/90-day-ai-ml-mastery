# Day 11 - Logistic Regression From Scratch

## What I Built
Logistic regression classifier to predict student pass/fail based on study hours.

## What I Learned
- Sigmoid function: 1 / (1 + e^(-x)) → converts any number to 0-1 probability
- Binary Cross Entropy loss punishes confident wrong predictions harder than MSE
- Decision boundary at 0.5 → above = PASS, below = FAIL
- 0 study hours → 1.15% pass probability (model learned this from data alone)

## Result
Student studying 6 hours → 68.78% pass probability → PASS ✅

## Tech Used
Python, NumPy, Matplotlib

## Key Formula
sigmoid(x) = 1 / (1 + e^(-x))
