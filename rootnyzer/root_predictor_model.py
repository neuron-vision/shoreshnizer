'''
The Neural network to predict clusters length -> root indices.
'''

import json
from pandas import DataFrame
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from pathlib import Path as _P
from rootnyzer.rootnyzer_dataset import WordClusterDataset
import os

ROOT_FOLDER = _P(os.path.abspath(__file__)).parent.parent
default_weights_path = _P('rootenizer/word_cluster_model.pth')


# Define the neural network architecture
class WordClusterPredictor(nn.Module):
    def __init__(self, weights_path:_P=default_weights_path, input_size=10, output_size=6, hidden_size=10):        
        super(WordClusterPredictor, self).__init__()
        self.output_size = output_size
        self.weights_path = weights_path

        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

        try:
            weights  = torch.load(weights_path)
            self.load_state_dict(weights)
            print(f"Loaded weights from {weights_path}")
        except BaseException as e:
            print(f"Did not load weights from {weights_path} due to {e}")
        self.eval()  # Default is eval


    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

    def train_loop(self, word_cluster_dataset):

        # Define loss function and optimizer
        criterion = nn.MSELoss()
        optimizer = optim.SGD(self.parameters(), lr=0.001)

        # Create DataLoader for the dataset
        dataloader = DataLoader(word_cluster_dataset, batch_size=1, shuffle=True)
        self.train()

        # Training loop
        num_epochs = 10
        for epoch in range(num_epochs):
            for words, lengths in dataloader:
                optimizer.zero_grad()
                inputs = torch.Tensor(words)  # Convert words to tensor
                targets = torch.Tensor(lengths)  # Convert lengths to tensor

                # Forward pass
                outputs = self(inputs)

                # Compute loss
                loss = criterion(outputs.squeeze(), targets)

                # Backward pass and optimization
                loss.backward()
                optimizer.step()

            print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item()}')

        # Save the trained model
        torch.save(self.state_dict(), default_weights_path)
        print(f"Model was saved to {default_weights_path}")




if __name__ == "__main__":

    dataset = WordClusterDataset()
    output_size = dataset.get_output_size()
    word, labels = dataset[0]

    self = WordClusterPredictor(output_size=output_size)
    output = self(word)
    print("labels", labels)    
    print("output", output)
    self.train_loop(dataset)

    # Example usage of the trained model
    the_word = 'הלכו'
    input_vec = dataset.get_input_vectors_for_word(the_word)
    predicted_length = self(input_vec)
    predicted_length = predicted_length.detach().cpu().numpy()
    print(f'{the_word} {predicted_length}')
