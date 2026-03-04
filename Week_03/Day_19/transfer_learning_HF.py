#imports
import os
import torch
import numpy as np
from torch.optim import AdamW
from transformers import AutoTokenizer, AutoModelForSequenceClassification

#hugging face time out
os.environ["HF_HUB_DOWNLOAD_TIMEOUT"] = "120" 

#load pretrained tokenizer and model
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels = 2
)

print(f"Model Loaded")
print(f"Parameters: {sum(p.numel() for p in model.parameters()):, }")

#simple sentiment data
texts = [
    "I love this product, it is amazing",
    "This is the best thing I ever bought",
    "Absolutely wonderful experience",
    "Great quality and fast delivery",
    "I am very happy with this purchase",
    "This is terrible, waste of money",
    "Worst product I have ever used",
    "Very disappointed, does not work",
    "Horrible experience, never buying again",
    "Complete garbage, avoid this",
]

labels = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0] #lables for it 1= +ve, 0=-ve

#tokenizer
def tokenize(texts, tokenizer, max_length=64):
    return tokenizer(
        texts,
        padding = True,
        truncation =True,
        max_length=max_length,
        return_tensors = "pt"
    )

encodings = tokenize(texts, tokenizer)
labels_tensor = torch.tensor(labels)

print(f"\nInput shape: {encodings['input_ids'].shape}")
print(f"Tokenized example: {tokenizer.decode(encodings['input_ids'][0])}")

#fine tune
optimizer = AdamW(model.parameters(), lr = 2e-5)

model.train()
print("\nFine tuning started")

for epoch in range(5):
    optimizer.zero_grad()

    output = model(
        input_ids = encodings['input_ids'],
        attention_mask = encodings["attention_mask"],
        labels = labels_tensor
    )

    loss = output.loss
    loss.backward()
    optimizer.step()

    #calculator
    predictions = torch.argmax(output.logits, dim=1)
    accuracy = (predictions == labels_tensor).float().mean()

    print(f"Epoch {epoch+1} | Loss: {loss.item():.4f} | Accuracy: {accuracy:.2%}")

#test on new data
model.eval()

test_sentences = [
    "This product exceeded my expectations",
    "I regret buying this, total waste",
    "Outstanding quality, highly recommend",
    "Broken on arrival, very frustrated",
    "decent product"
]

print("\nPredictions on new sentences:")
print("-" * 50)

with torch.no_grad():
    test_encodings = tokenize(test_sentences, tokenizer)
    output = model(**test_encodings)
    predictions = torch.argmax(output.logits, dim=1)
    probabilities = torch.softmax(output.logits, dim=1)

    for i ,sentence in enumerate(test_sentences):
        label = "POSITIVE" if predictions[i] == 1 else "NEGATIVE"
        confidence = probabilities[i][predictions[i]].item()
        print(f"'{sentence}'")
        print(f"→ {label} ({confidence:.2%} confident)\n")

#save fine tuned model
model.save_pretrained("./sentiment_model")
tokenizer.save_pretrained("./sentiment_model")
print("Fine-tuned model saved ")