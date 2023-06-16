'''
Author: Ishay Tubi, Neuron Vision
Date: June 14, 2023
Description: This class is used to predict root index for a given work.
First we use a dictionary and rule based until we can train one.


Discussion:
Which architecture is best fit for function which receveis a word with arcitrary length
and returns and array of indices (length 3-5) per root letter locations.
e.g.
F('יהלכו') -> [1, 2, 3]
F('יושיבו') -> [0, 2, 4]

Suggestion:
Output is always an array of maximum length 4 (support up to 4 letters root).
4 * 4 matrix: 

location                         |  loc 0 |  loc 1  |  loc 2  | loc 3 |
prob for index is the 1st letter |        |         |         |       |
prob for index is the 2nd letter |        |         |         |       |
prob for index is the 3ed letter |        |         |         |       |
prob for index is the 4th letter |        |         |         |       |

Once matrix probs are known we can select a legal combination with highest likelihood.


'''



#Another Suggestion: There are only a small number of legal permutations:

possible_root_indices_arrangements = [
[0, 1, 2], #  ישבנו
[1, 2, 3], #  והלכנו
[2, 3, 4], #  התישבנו
[3, 4, 5], #
[4, 5, 6], #
[4, 6, 7], #
[4, 5, 7], #
[3, 3, 5], #  להושיב אין יוד של השורש ולכן נבלעה עם השין
[0, 2, 3] #  יושבים
# [?, ?, ?]  #TODO: What other are legal combinations exist?
# 6 possible combinations is a smaller space then above 4*4 representation 
]


from pathlib import Path as _P
import os
import json
from typing import Tuple, List
from word_break_down import WordBreakDown
from rootenizer.rootenizer_utils import remove_characters


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


if __name__ == "__main__":
    #Create all possbile indices combincations for root.

    combinations = []
    for p in range(0, 5):
        for r1 in range(p, p+1):
            for i1 in range(r1, r1+2):
                for r2 in range(i1, i1+1):
                    for i2 in range(r2, r2+1):
                        for r3 in range(i2, i2+1):
                            d = dict(
                                p=p,
                                r1=r1,
                                i1=i1,
                                r2=r2,
                                i2=i2,
                                r3=r3
                            )
                            combinations.append(d)

    print(f"Found Total of {len(combinations)} combinations.")
    for i, combination in enumerate(combinations):
        print(f"{i:4}\t{combination}")
