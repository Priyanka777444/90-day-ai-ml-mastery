#imports
import numpy as np
import matplotlib.pyplot as plt

#activation function

def relu(x):
    return np.maximum(0,x)

def relu_derivative(x):
    return (x>0).astype(float)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    s = sigmoid(x)
    return s*(1-s)

#initilize network

def init_network(input_size, hidden_size, output_size):
    np.random.seed(42)
    network = {
        'W1': np.random.randn(input_size, hidden_size) * np.sqrt(2 / input_size),
        'b1':np.zeros((1, hidden_size)),
        'W2': np.random.randn(hidden_size, output_size) * np.sqrt(2 / hidden_size),
        'b2':np.zeros((1, output_size))
    }

    return network

#forward pass
def forward_pass(X, network):
    #layer1
    Z1 = np.dot(X, network['W1']) + network['b1']
    A1  =relu(Z1)

    #layer2
    Z2 = np.dot(A1, network['W2']) + network['b2']
    A2  =sigmoid(Z2)

    cache = {'Z1':Z1, 'A1':A1, 'Z2':Z2, 'A2':A2}
    return A2, cache

#loss
def compute_loss(y_true, y_pred):
    n = len(y_true)
    loss  =-np.mean(y_true*np.log(y_pred + 1e-9)+
                        (1 - y_true)*np.log(1 - y_pred + 1e-9))
    return loss

#backpropagation
def backward_pass(X, y, network, cache):
    n =len(X)
    A1, A2 = cache['A1'], cache['A2']
    Z1 = cache['Z1']

    #output layer gradient
    dA2 = -(y/(A2 + 1e-9)) + (1-y)/(1-A2+ 1e-9)
    dZ2 = dA2*sigmoid_derivative(cache['Z2'])
    dW2 = np.dot(A1.T, dZ2)/n
    db2 = np.mean(dZ2, axis = 0, keepdims=True)

    #hidden layer
    dA1 = np.dot(dZ2, network['W2'].T)
    dZ1 = dA1*relu_derivative(Z1)
    dW1 = np.dot(X.T, dZ1)/n
    db1 = np.mean(dZ1, axis = 0, keepdims=True)

    gradient = {'dW1':dW1, 'db1': db1, 'dW2': dW2, 'db2': db2}
    return gradient

#update weights
def up_weights(network, gradient, lr=0.01):
    network['W1'] -= lr*gradient['dW1']
    network['b1'] -= lr*gradient['db1']
    network['W2'] -= lr*gradient['dW2']
    network['b2'] -= lr*gradient['db2']

    return network

#training loop 
def train(X, y, hidden_size = 8, epochs = 1000, lr = 0.01):
    network = init_network(X.shape[1], hidden_size, 1)
    loss_h = []

    for e in range(epochs):
        y_pred, cache = forward_pass(X, network)
        loss = compute_loss(y, y_pred)
        loss_h.append(loss)
        gradient = backward_pass(X, y , network, cache)
        network = up_weights(network, gradient, lr)

        if e % 100 == 0:
            print(f"Epoch{e}| Loss:{loss:.4f}")
    
    return network, loss_h

#test it
# XOR problem (classic NN test)
X = np.array([[0,0], [0,1], [1,0], [1,1]])
y = np.array([[0], [1], [1], [0]])  # XOR output

network, loss_h= train(X, y, hidden_size=8, epochs=10000, lr=0.1)

# Plot loss
plt.plot(loss_h, color='green')
plt.title("Neural Network Loss - XOR Problem")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.savefig("result.png")
plt.show()

#final prediction
y_pred, _ = forward_pass(X, network)
print("\nXOR Predictions:")
for i in range(len(X)):
    print(f"{X[i]} → Expected: {y[i][0]} | Predicted: {y_pred[i][0]:.4f} | {'✅' if round(y_pred[i][0]) == y[i][0] else '❌'}")
