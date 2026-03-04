# Day 18 - Real Dataset + Train/Test Split in PyTorch

## What I Built
Cancer detection classifier using PyTorch on real breast cancer dataset.
569 samples, 30 features, binary classification.

## What I Learned
- Always split data BEFORE scaling (prevent data leakage)
- fit_transform on train, only transform on test
- model.train() → Dropout active → prevents overfitting
- model.eval() + torch.no_grad() → Dropout disabled → for inference
- Train vs Test accuracy gap = overfitting detector
- torch.save() → saves model weights for later use

## Result
Train Accuracy: 99.12%
Test Accuracy:  98.25%
Gap: 0.87% → No overfitting ✅

## Tech Used
Python, PyTorch, Scikit-learn

## Key Concept
Dropout = randomly kill neurons during training
Forces network to learn robust features, not memorize