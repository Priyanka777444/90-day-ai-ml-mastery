# Day 12 - Decision Tree From Scratch

## What I Built
Decision Tree classifier to predict student pass/fail 
based on study hours and attendance.

## What I Learned
- Gini Impurity: measures how mixed/impure a node is
- Tree picks the split that reduces Gini the most
- Recursion builds the tree naturally — each node asks a question
- max_depth prevents overfitting (tree stops growing)
- Generator () vs List [] behave completely differently

## Result
Accuracy: 99.50%
- 2hrs study, 30% attendance → FAIL ❌
- 8hrs study, 90% attendance → PASS ✅  
- 5hrs study, 50% attendance → PASS ✅

## Tech Used
Python, NumPy, Collections

## Key Concept
Gini = 1 - Σ(probability of each class)²
Pure node = 0, Maximum impurity = 0.5