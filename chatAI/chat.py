import random
import json
import torch

from chatAI.torchchat import NeuralNet
from chatAI.nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load intents
try:
    with open('chatAI/chat.json', 'r') as json_data:
        intents = json.load(json_data)
except FileNotFoundError:
    print("Intent file not found. Please check the path.")
    exit()

# Load model data
FILE = "data.pth"
try:
    data = torch.load(FILE)
except FileNotFoundError:
    print("Model data file not found. Please check the path.")
    exit()

input_size = data["input_size"] 
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

# Initialize model
model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Testla"
def get_response(msg):
    # Normalize input
    msg = msg.lower()
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    # Debugging outputs
    print(f"Input: {msg}")
    print(f"Tokenized: {sentence}")
    print(f"Bag of Words: {X}")
    print(f"Predicted Tag: {tag}, Confidence: {prob.item()}")

    if prob.item() > 0.8:  # Confidence threshold
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])

    return "I'm not quite sure about that. Can you clarify or ask something else?"

if __name__ == "__main__":
    print(f"{bot_name}: Hello! How can I assist you today?")
    while True:
        sentence = input("You: ")
        if sentence.lower() == "quit":
            print(f"{bot_name}: Goodbye! Have a great day!")
            break

        resp = get_response(sentence)
        print(f"{bot_name}: {resp}")