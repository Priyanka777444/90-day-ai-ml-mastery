"""
By Priyanka 
"""

#step 1 imports 
import numpy as np
import matplotlib.pyplot as plt

#step 2 sigmoid function

def sigmoid(x):
    return 1/(1+np.exp(-x))

#step 3 generate student data
np.random.seed(42)
study_hours = np.random.uniform(0, 10, 100)
passed = (study_hours + np.random.normal(0, 1.5, 100) > 5).astype(int)

#step 4 initilize weights
w = 0.0
b = 0.0
lr = 0.1
epochs = 1000
n = len(study_hours)

#step 5 start training  loop
loss_h = []

for epoch in range(epochs):
    #linera combination
    z = w *study_hours + b

    #pass through sigmoid
    y_pred = sigmoid(z)

    #binary cross entropy loss
    loss = -np.mean(passed *np.log(y_pred + 1e-9) + (1 - passed )* np.log(1 - y_pred + 1e-9))
    loss_h.append(loss)

    #gradients
    dw = np.mean((y_pred - passed) * study_hours)
    db = np.mean(y_pred - passed)

    #update
    w = w - lr * dw
    b = b - lr * db

    if epoch % 100 == 0:
        print(f"Epoch {epoch} | Loss: {loss:.4f} | w: {w:.4f} | b: {b:.4f}")

#step 6 plot + predict 
plt.figure(figsize=(12, 4))

# Plot 1 - decision boundary
plt.subplot(1, 2, 1)
plt.scatter(study_hours, passed, color='blue', alpha=0.5, label='Actual')
x_line = np.linspace(0, 10, 100)
y_line = sigmoid(w * x_line + b)
plt.plot(x_line, y_line, color='red', label='Sigmoid Curve')
plt.axhline(y=0.5, color='green', linestyle='--', label='Decision Boundary')
plt.xlabel("Study Hours")
plt.ylabel("Pass Probability")
plt.title("Logistic Regression From Scratch")
plt.legend()

# Plot 2 - loss curve
plt.subplot(1, 2, 2)
plt.plot(loss_h, color='green')
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Loss Decreasing")

plt.tight_layout()
plt.savefig("result.png")
plt.show()

# Test prediction
test_hours = 6
probability = sigmoid(w * test_hours + b)
print(f"\nStudent studying {test_hours} hours → Pass probability: {probability:.2%}")
print(f"Prediction: {'PASS ✅' if probability > 0.5 else 'FAIL ❌'}")