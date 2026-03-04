#import
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

#data same xor as before
X = torch.tensor([[0,0],[0,1],[1,0],[1,1]], dtype=torch.float32)
y = torch.tensor([[0],[1],[1],[0]], dtype=torch.float32)

#network compare 
class XORNet(nn.Module):

    def __init__(self,):
        super().__init__()
        self.layer1 = nn.Linear(2,16)
        self.layer2 = nn.Linear(16,8)
        self.layer3 = nn.Linear(8,1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.relu(self.layer2(x))
        x = self.sigmoid(self.layer3(x))
        return x
    
model = XORNet()
criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr = 0.01)

#transition loop
loss_h = []

for epoch in range(5000):
    #forward pass
    y_pred = model(X)
    loss = criterion(y_pred,y)
    loss_h.append(loss.item())

    #backward pass 
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 500 == 0:
        print(f"Epoch {epoch} | Loss: {loss.item():.4f}")

#plot
plt.plot(loss_h, color='green')
plt.title("PyTorch XOR - Loss Curve")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.savefig("result.png")
plt.show()

# Predictions
print("\nPredictions:")
with torch.no_grad():
    predictions = model(X)
    for i in range(len(X)):
        pred = predictions[i].item()
        expected = y[i].item()
        print(f"{X[i].tolist()} → Expected: {int(expected)} | Predicted: {pred:.4f} | {'✅' if round(pred)==int(expected) else '❌'}")

# Count parameters
total_params = sum(p.numel() for p in model.parameters())
print(f"\nTotal trainable parameters: {total_params}")
