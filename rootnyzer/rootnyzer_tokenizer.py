'''
Author: Ishay Tubi, Neuron Vision
Date: June 14, 2023
Description: 
Running this class allows receiving a word or a collection of words and
obtain a vector representation per word while preserving semantic meaning.
'''

from pathlib import Path as _P
import os
import json
from typing import Tuple, List
from word_break_down import WordBreakDown
from rootnyzer_utils import character_index


class rootnyzerTokenizer(object):
    '''
    Predict the root of each root and cluster all the rest of the characters.
    '''
    def __init__(self, root_predictor) -> None:
        self.root_predictor = root_predictor
        # Hardcoded params to be moved out to configuration file later:
        self.total_number_of_bits_per_word = 32  
        self.number_of_bits = dict(
            root = 5,  # Number of bits used for a single root char.
            infix = 2,
            prefix = 4,
            suffix = 4,
            other = 7  # Special chars
        )


    def embed(self, breakdown:WordBreakDown):
        '''
        Convert a breakdown dict into a 32 unsigned integer.
        '''
        # Start with root chars.
        embedding = 0
        root_bit_mask = (2**self.number_of_bits['root'] -1)
        for i, char in enumerate(breakdown.root):
            char_index = character_index(char) + 1  # Preserve 0 for no value, start with 1 for exiting value.
            char_index = char_index % root_bit_mask  # Avoid overflow
            embedding += char_index
            embedding <<= self.number_of_bits['root']
            if i >= 2: break  # TODO: we only support 3 chars per root for now.
        
        # Embed infix chars (4 bit)
        infix_translation = {
            'יו':3,
            'וי':3,
            'י':1,
            'ו':2,
            '':0
        }
        infix_val = infix_translation.get(breakdown.infix, 0)
        embedding += infix_val
        embedding <<= self.number_of_bits['infix']

        # TODO: Quantize prefix to 4 bits: placeholder logic until replaced.
        suffix_val = sum([ord(char)-ord('א') for char in breakdown.suffix])
        suffix_val &= (2**self.number_of_bits['suffix'] -1) # modulo with allowed number of bits.
        embedding += suffix_val
        embedding <<= self.number_of_bits['suffix']

        # TODO: Quantize prefix to 4 bits: placeholder logic until replaced.
        prefix_val = sum([ord(char)-ord('א') for char in breakdown.prefix])
        prefix_val &= (2**self.number_of_bits['prefix'] -1) # modulo with allowed number of bits.
        embedding += prefix_val
        embedding <<= self.number_of_bits['prefix']

        # TODO: Add spacial chars for remaining 7 bit
        other_val = 0 
        embedding += other_val
        embedding <<= self.number_of_bits['prefix']
        return embedding


    def __call__(self, sentence:str) -> Tuple[List[int], List[WordBreakDown]]:
        ''' 
        Input: A sentence with multiple words separated with spaces.
        Output: List of dictionary breakdown per word.
        '''
        words = sentence.split()
        breakdowns_list = []  # The returning value
        embedding_list = []
        for word in words:
            breakdown = self.root_predictor(word)
            breakdowns_list.append(breakdown)

            embedding = self.embed(breakdown)
            embedding_list.append(embedding)
        return embedding_list, breakdowns_list
    
    def html(self, list_of_breakdowns) ->str:
        '''
        Utility to dump tokens with html colors
        '''
        css = "<style> \n \
                .prefix  {background-color: green;} \n\
                .root {background-color: yellow;} \n\
                .infix {background-color: orange;} \n\
                .suffix {background-color: red;} \n\
                </style>\n"
        html = '' + css + "\n"
        for b in list_of_breakdowns:
            message = \
                f"<span class=prefix>{b.prefix}</span> \
                <span class=root>{b.root}</span> \
                <span class=infix>{b.infix}</span> \
                <span class=suffix>{b.suffix}</span>"

            html = html + "</br>\n" + message
        return html
    
    def train(self):
        '''
        Minimize reconstruction error, Show that the error is minimized as a factor of context length. 
        '''
        raise BaseException("מימוש חסר")
    
    def stats(self):
        '''
        plot algorithm statistics for research.
        '''


if __name__ == '__main__':
    from rootnyzer.rootnyzer_dataset import WordClusterDataset
    from rootnyzer.root_predictor import RootPredictor
    dataset = WordClusterDataset()
    root_predictor = RootPredictor()
    index = 0
    key = dataset.data_table.index[index]
    row = dataset.data_table.iloc[index]
    word, clusters = key, row[['P', 'R1', 'I1', 'R2', 'I2', 'R3']].values.astype('float32')
    tensor, clusters_length = dataset[0]
    print(key, tensor, clusters_length)

    self = rootnyzerTokenizer(root_predictor)
    #Lets visualize the dataset with colors.
    the_sentence = "משפט שנקצה לפרק"
    embedding_list, breakdowns_list = self(the_sentence)
    print(the_sentence)
    for breakdown, embeddings in zip(breakdowns_list, embedding_list):
        print(breakdown, embeddings)
