# Day 13 - Random Forest From Scratch

## What I Built
Random Forest classifier built on top of my Day 12 Decision Tree.
10 trees trained on random bootstrap samples, majority voting for prediction.

## What I Learned
- Bootstrap sampling = random sampling WITH replacement
- Each tree sees different data = diversity = better predictions
- Same data for all trees = no diversity = pointless forest
- Ensemble learning: combine weak models to make strong model
- Random Forest doesn't always beat single tree on clean simple data

## Result
Single Decision Tree: 99.50%
Random Forest (10 trees): 99.00%
Lesson: Forest shines on noisy real-world data, not clean synthetic data

## Tech Used
Python, NumPy, Collections

## Key Concept
Ensemble Learning = many weak learners → one strong learner
Bootstrap = sample WITH replacement = diversity