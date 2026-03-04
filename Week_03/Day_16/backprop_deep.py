#imports
import numpy as np
import matplotlib.pyplot as plt

#activation fun
def relu(x):
    return np.maximum(0,x)

def relu_derivative(x):
    return (x>0).astype(float)

def sigmoid(x):
    return 1/(1 + np.exp(-x))

#layer network deeper
def init_network(input_size, h1_size, h2_size, output_size):
    np.random.seed(42)
    return {
        'W1': np.random.randn(input_size, h1_size) * np.sqrt(2/input_size),
        'b1': np.zeros((1, h1_size)),
        'W2': np.random.randn(h1_size, h2_size) * np.sqrt(2/h1_size),
        'b2': np.zeros((1, h2_size)),
        'W3': np.random.randn(h2_size, output_size) * np.sqrt(2/h2_size),
        'b3': np.zeros((1, output_size))
    }

#forward pass(3layers)
def forward_pass(X, net):
    Z1 = np.dot(X, net['W1']) + net['b1']
    A1 = relu(Z1)
    
    Z2 = np.dot(A1, net['W2']) + net['b2']
    A2 = relu(Z2)
    
    Z3 = np.dot(A2, net['W3']) + net['b3']
    A3 = sigmoid(Z3)
    
    cache = {'Z1':Z1,'A1':A1,'Z2':Z2,'A2':A2,'Z3':Z3,'A3':A3}
    return A3, cache

#Backward Pass (chain rule through 3 layers):

def backward_pass(X, y, net, cache):
    n = len(X)
    A1,A2,A3 = cache['A1'],cache['A2'],cache['A3']
    
    # Layer 3 gradients
    dZ3 = A3 - y
    dW3 = np.dot(A2.T, dZ3) / n
    db3 = np.mean(dZ3, axis=0, keepdims=True)
    
    # Layer 2 gradients (chain rule)
    dA2 = np.dot(dZ3, net['W3'].T)
    dZ2 = dA2 * relu_derivative(cache['Z2'])
    dW2 = np.dot(A1.T, dZ2) / n
    db2 = np.mean(dZ2, axis=0, keepdims=True)
    
    # Layer 1 gradients (chain rule again)
    dA1 = np.dot(dZ2, net['W2'].T)
    dZ1 = dA1 * relu_derivative(cache['Z1'])
    dW1 = np.dot(X.T, dZ1) / n
    db1 = np.mean(dZ1, axis=0, keepdims=True)
    
    return {'dW1':dW1,'db1':db1,'dW2':dW2,'db2':db2,'dW3':dW3,'db3':db3}

#update weights
def update(net, grads, lr):
    for key in ['W1','b1','W2','b2','W3','b3']:
        net[key] -= lr * grads['d'+key]
    return net

#train
def train(X, y, epochs=10000, lr=0.01):
    net = init_network(2, 16, 8, 1)
    loss_h = []
    grad_magnitudes = []  # track how gradients flow

    for epoch in range(epochs):
        A3, cache = forward_pass(X, net)
        
        # loss
        loss = -np.mean(y * np.log(A3+1e-9) + (1-y) * np.log(1-A3+1e-9))
        loss_h.append(loss)
        
        grads = backward_pass(X, y, net, cache)
        
        # track gradient magnitude per layer
        grad_magnitudes.append([
            np.mean(np.abs(grads['dW1'])),
            np.mean(np.abs(grads['dW2'])),
            np.mean(np.abs(grads['dW3']))
        ])

        net = update(net, grads, lr)

        if epoch % 1000 == 0:
            print(f"Epoch {epoch} | Loss: {loss:.4f}")
    
    return net, loss_h, np.array(grad_magnitudes)

#test +visiulize

X = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([[0],[1],[1],[0]])

net, loss_h , grad_magnitudes = train(X,y)

plt.figure(figsize=(14, 4))

# Plot 1 - Loss
plt.subplot(1, 3, 1)
plt.plot(loss_h, color='green')
plt.title("Loss Curve")
plt.xlabel("Epoch")
plt.ylabel("Loss")

# Plot 2 - Gradient flow per layer
plt.subplot(1, 3, 2)
plt.plot(grad_magnitudes[:, 0], label='Layer 1', color='red')
plt.plot(grad_magnitudes[:, 1], label='Layer 2', color='blue')
plt.plot(grad_magnitudes[:, 2], label='Layer 3', color='green')
plt.title("Gradient Flow Per Layer")
plt.xlabel("Epoch")
plt.ylabel("Gradient Magnitude")
plt.legend()

# Plot 3 - Final predictions
plt.subplot(1, 3, 3)
A3, _ = forward_pass(X, net)
colors = ['red' if p > 0.5 else 'blue' for p in A3.flatten()]
plt.scatter(X[:,0], X[:,1], c=colors, s=200)
plt.title("XOR Decision (Red=1, Blue=0)")
plt.xlabel("Input 1")
plt.ylabel("Input 2")

plt.tight_layout()
plt.savefig("result.png")
plt.show()

print("\nFinal Predictions:")
for i in range(len(X)):
    print(f"{X[i]} → Expected: {y[i][0]} | Predicted: {A3[i][0]:.4f} | {'✅' if round(A3[i][0])==y[i][0] else '❌'}")