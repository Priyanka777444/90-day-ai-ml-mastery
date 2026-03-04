#imports
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

#load real data
# Breast cancer dataset - predict malignant vs benign
data = load_breast_cancer()
X, y = data.data, data.target

print(f"Dataset Shape: {X.shape}")
print(f"Features:{data.feature_names[:5]}")
print(f"Classes: {data.target_names}")
print(f"Malignant: {sum(y==0)}, Benign: {sum(y==1)}")

#preprocess
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#scale features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train) # fit+transform on train
X_test = scaler.transform(X_test) # transform on test

#convert to tensors
X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype = torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
y_test = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)

print(f"\nTrain size: {X_train.shape[0]}")
print(f"Test size: {X_test.shape[0]}")

#build network
class CancerNet(nn.Module):
    def  __init__(self, input_size):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(32,1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.network(x)
    
model = CancerNet(X_train.shape[1])
print(f"\nModel parameters: {sum(p.numel() for p in model.parameters())}")

#training with train and test data
criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr = 0.001)

train_losses = []
test_losses = []
train_acc = []
test_acc = []

def get_acc(y_pred, y_true):
    predicted = (y_pred>0.5).float()
    return (predicted == y_true).float().mean().item()

for epoch in range(200):
    #training model
    model.train()
    y_pred_train = model(X_train)
    train_loss = criterion(y_pred_train, y_train)

    optimizer.zero_grad()
    train_loss.backward()
    optimizer.step()

    #Eavalution model
    model.eval()
    with torch.no_grad():
        y_pred_test = model(X_test)
        test_loss = criterion(y_pred_test, y_test)

        train_accuracy = get_acc(y_pred_train, y_train)
        test_accuracy = get_acc(y_pred_test, y_test)

        train_losses.append(train_loss.item())
        test_losses.append(test_loss.item())
        train_acc.append(train_accuracy)
        test_acc.append(test_accuracy)

        if epoch %20 == 0:
            print(f"Epoch: {epoch} | Train Loss: {train_loss.item():.4f} | Test Loss: {test_loss.item():.4f} | Train Accuracy: {train_accuracy:.2%} | Test Accuracy: {test_accuracy:.2%}")

#plot 
plt.figure(figsize=(12,4))
plt.plot(train_losses, label = 'Train Loss', color = 'blue')
plt.plot(test_losses, label = 'Test Loss', color = 'red')
plt.title("Train vs Test Loss")
plt.xlabel("Epoch")
plt.legend()

plt.subplot(1,2,2)
plt.plot(train_acc, label = "Train Accuracy", color = 'blue')
plt.plot(test_acc, label = 'Test Accuracy', color = 'red')
plt.title("Train vs Test Accuracy")
plt.xlabel("Epoch")
plt.legend()

plt.tight_layout()
plt.savefig("result.png")
plt.show()

print(f"\nFinal Train Accuracy: {train_acc[-1]:.2%}")
print(f"Final Test Accuracy:  {test_acc[-1]:.2%}")

#save model
torch.save(model.state_dict(), "cancer_model.pth")
print("Model saved as cancer_model.pth")




