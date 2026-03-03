#step 1 imports
import numpy as np
import matplotlib.pyplot as plt

#step 2 data 
np.random.seed(42)
experience = np.random.uniform(0, 10, 50) #0-10 years
salary = 30000 + (5000 * experience) + np.random.normal(0, 5000, 50) #noise added

#step 3 initilize weights
w = 0.0  # slope
b = 0.0  # intercept
lr = 0.01  # learning rate 
epochs = 1000  # how many times we adjust
n = len(experience)

#step 4 the heart
loss_history = []

for epoches in range(epochs):
    #predict
    y_pred = w*experience + b

    #calculate loss (Mean Square Error MSE)
    loss = (1/n)*np.sum((salary - y_pred)**2)
    loss_history.append(loss)

    # calculate gradients (this is the slope of the hill)
    dw = (-2/n) * np.sum(experience * (salary - y_pred))
    db = (-2/n) * np.sum(salary - y_pred)

    # update weights (take a small step downhill)
    w = w - lr * dw
    b = b - lr * db

    if epoches % 100 == 0:
        print(f"Epoch {epoches} | Loss: {loss:.2f} | w: {w:.2f} | b: {b:.2f}")

# step 5 plot results:

plt.figure(figsize=(12, 4))

# Plot 1 - regression line
plt.subplot(1, 2, 1)
plt.scatter(experience, salary, color='blue', alpha=0.5, label='Real Data')
plt.plot(experience, w * experience + b, color='red', label='Our Prediction')
plt.xlabel("Experience (years)")
plt.ylabel("Salary (₹)")
plt.title("Linear Regression From Scratch")
plt.legend()

# Plot 2 - loss going down
plt.subplot(1, 2, 2)
plt.plot(loss_history, color='green')
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Loss Decreasing = Gradient Descent Working")

plt.tight_layout()
plt.savefig("result.png")
plt.show()

print(f"\nFinal: Salary = {w:.0f} * experience + {b:.0f}")



