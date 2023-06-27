'''
Author: Ishay Tubi, Neuron Vision. 2023.
Description:
Rootenizer dataset translating word into vector reps and the root indices.
'''

import torch
from torch.utils.data import Dataset
from pathlib import Path as _P

from pandas import DataFrame, read_csv

dataset_path = _P('rootenizer/rootenizer - Dataset.csv')


def load_dataset(dataset_path=dataset_path):
    data = read_csv(dataset_path).set_index('Word')
    return data


# Custom dataset class.
class WordClusterDataset(Dataset):
    '''
    We will try to use the ascii encoding instead of 1 hot encoding for a compact representation.
    '''

    def __init__(self, data:DataFrame=None, max_input_length=10):
        self.data_table = data or load_dataset()
        self.max_input_length = max_input_length

    def get_output_size(self):
        '''
        '''
        word, cluster_length = self[0] 
        return len(cluster_length) 
    
    def get_input_vectors_for_word(self, word):
        '''
        Translate the string into an input vector. 
        '''
        t = torch.zeros(self.max_input_length, dtype=torch.float32)
        for i, c in enumerate(word):
            t[i] = ord(c)
        return t

    def __len__(self):
        return len(self.data_table)

    def __getitem__(self, index):
        word = self.data_table.index[index]
        row = self.data_table.loc[word]
        values = row[['P', 'R1', 'I1', 'R2', 'I2', 'R3']].values.astype('float32')
        values = torch.from_numpy(values)
        t= self.get_input_vectors_for_word(word)
        return t, values
    
    def augment_with_data(self):
        '''
        Load the 3 letters root and iteate with

        '''


if __name__ == '__main__':
    self = WordClusterDataset()
    index = 0
    key = self.data_table.index[index]
    row = self.data_table.iloc[index]
    word, clusters = key, row[['P', 'R1', 'I1', 'R2', 'I2', 'R3']].values.astype('float32')
    tensor, clusters_length = self[0]
    print(key, tensor, clusters_length)
    

