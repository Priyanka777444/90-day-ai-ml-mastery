#step 1 imports
import numpy as np
from collections import Counter

# step 2 gini impurity
def gini(y):
    classes = Counter(y)
    n = len(y)
    return 1- sum((count/n)**2 for count in classes.values())

# step 3 best split finder

def best_split(X,y):
    best_gini = float('inf')
    best_feature = None
    best_threshold = None

    for feature in range(X.shape[1]):
        threshold = np.unique(X[:,feature])

        for t in threshold:
            left_mask = X[:, feature]<= t
            right_mask = ~left_mask

            if sum(left_mask) == 0 or sum(right_mask) == 0:
                continue
            left_gini = gini(y[left_mask])
            right_gini = gini(y[right_mask])

             # weighted gini
            n = len(y)
            weighted = (sum(left_mask)/n * left_gini + 
                       sum(right_mask)/n * right_gini)
            
            if weighted < best_gini:
                best_gini = weighted
                best_feature = feature
                best_threshold = float(t)
    
    return best_feature, best_threshold

# step 4 tree node
class Node:
    def __init__(self, feature=None, threshold=None, 
                 left=None, right=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value  # only for leaf nodes

#step 5 build tree recursively
def build_tree(X, y, depth=0, max_depth=5):
    #stopping conditions
    if len(set(y)) == 1 or depth == max_depth or len(y)<2:
        leaf_value = Counter(y).most_common(1)[0][0]
        return Node(value=leaf_value)
    
    feature, threshold = best_split(X,y)

    if feature is None:
        leaf_value = Counter(y).most_common(1)[0][0]
        return Node(value=leaf_value)
    
    left_mask = X[:,feature]<=threshold
    right_mask = ~left_mask
    left = build_tree(X[left_mask], y[left_mask], depth+1, max_depth)
    right = build_tree(X[right_mask], y[right_mask], depth+1, max_depth)

    return Node(feature=feature, threshold=threshold, left=left, right=right)

# step 6 predict 
def predict_one(node,x):
    if node.value is not None:
        return node.value
    
    if float(x[node.feature]) <= float(node.threshold):
        return predict_one(node.left, x)
    return predict_one(node.right, x)

def predict(tree,X):
    return [predict_one(tree,x) for x in X]

# step 7 test it

#generate student data
np.random.seed(42)
n = 200
study_hours = np.random.uniform(0, 10, n)
attendance = np.random.uniform(0, 100, n)
passed = ((study_hours * 0.6 + attendance * 0.04) > 5).astype(int)

X = np.column_stack([study_hours, attendance])
y = passed

# Build tree
tree = build_tree(X, y, max_depth=5)

# Predict
predictions = predict(tree, X)
accuracy = np.mean(predictions == y)
print(f"Accuracy: {accuracy:.2%}")


# Test cases
test_cases = [
    [2, 30],   # low study, low attendance
    [8, 90],   # high study, high attendance
    [5, 50],   # medium everything
]

print("\nPredictions:")
for case in test_cases:
    result = predict_one(tree, np.array(case))
    print(f"Study: {case[0]}hrs, Attendance: {case[1]}% → {'PASS ✅' if result == 1 else 'FAIL ❌'}")
