'''
Author: Ishay Tubi, Neuron Vision
Date: June 14, 2023
Description: This class us used to predict root index for a given work.
First we use a dictionary and rule based until we can train one.
'''

from pathlib import Path as _P
import os
import json
from typing import Tuple, List
from word_break_down import WordBreakDown
from rootenizer_utils import remove_characters


class RootPredictor(object):
    def __init__(self, voc_path:str=None) -> None:
        '''
        Use a dictionary and rule based until training data is gathered.
        '''
        self.voc_path = _P(voc_path or 'src/mini_shoreshnizer.json')
        self.shoresh_list = json.load(self.voc_path.open('rt'))
        print(f"Loaded {len(self.shoresh_list)} words with roots.")
    
    def __call__(self, word:str) -> WordBreakDown:
        '''
        Predict the root, assign all other chars with their correct clusters.
        '''

        word = word.strip()  # Remove blanks
        if word in self.shoresh_list:
            root, idx = self.shoresh_list[word]
        else:
            root, idx = word, range(len(word))  # TODO: fix this
        
        #Fallback 1: Apply fuzzy logic
        #Fallback 2: Select all as root for short words.
        #Fallback 3: Use char based?
        #If Not found, should the whole word be treated as a root?

        start, stop = idx[0], idx[-1]
        prefix = word[:start]  if start>0 else '' # Slice what ever starts before the root
        suffix = word[stop+1:]  # Slice what ever ends after the root
        no_suffix = word[:stop+1]  # Lets find all characters that are in the infix of roots, remove suffix, remove root, remove prefix and find infix chars.
        infix = remove_characters(no_suffix, idx)[start:]  # Remove the root and keep only what is left in the infix.
        return WordBreakDown(
            prefix=prefix,
            root=root,
            infix=infix,
            suffix=suffix
        )

