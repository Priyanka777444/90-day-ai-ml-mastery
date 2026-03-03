# Day 14 - K-Means Clustering From Scratch

## What I Built
K-Means clustering algorithm from scratch to find natural groups 
in data without any labels (unsupervised learning).

## What I Learned
- Unsupervised learning = no labels, model finds patterns itself
- K-Means: assign points to nearest centroid → move centroid → repeat
- np.allclose = checks if two arrays are almost equal (never use == for floats)
- Convergence = centroids stop moving = algorithm found the best clusters
- KNN (supervised) vs K-Means (unsupervised) — completely different

## Result
Cluster 1 centroid: (1.86, 1.93) → target was (2, 2) ✅
Cluster 2 centroid: (2.13, 8.00) → target was (2, 8) ✅
Cluster 3 centroid: (7.90, 8.14) → target was (8, 8) ✅

Model found all 3 clusters with no labels. Pure math.

## Tech Used
Python, NumPy, Matplotlib

## Key Concept
Unsupervised Learning = find patterns without labels
K-Means = minimize distance between points and their centroid
