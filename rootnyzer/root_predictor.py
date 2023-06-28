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
import sys



ROOT_FOLDER = _P(os.path.abspath(__file__)).parent.parent

ROOTS_HE_3_LETTERS = ROOT_FOLDER /'rootnyzer/[he]roots3_only.txt'
if str(ROOT_FOLDER) not in sys.path:
    sys.path.append(str(ROOT_FOLDER))


import os
import json
from typing import Tuple, List
from word_break_down import WordBreakDown
from rootnyzer.rootnyzer_utils import remove_characters



class RootPredictor(object):
    def __init__(self, voc_path:str=None) -> None:
        '''
        Use a dictionary and rule based until training data is gathered.
        '''
        self.voc_path = _P(voc_path or 'rootnyzer/mini_shoreshnizer.json')
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


    def generate_synth_data(self):
        '''
        Apply logic
        '''

    def generate_all_combinations(self):
        combinations = []
        #Each value states where the cluster ends.
        for p in [0, 1, 2, 3, 4, 5]:
            for r1 in [1]:
                for i1 in [0, 1, 2]:
                    for r2 in [1]:
                        for i2 in [0, 1, 2]:
                            for r3 in [1]:
                                d = dict(
                                    p=p,
                                    r1=r1+p,
                                    i1=i1+r1+p,
                                    r2=r2+i1+r1+p,
                                    i2=i2+r2+i1+r1+p,
                                    r3=r3+i2+r2+i1+r1+p
                                )
                                root_indices = d['r1'] - 1, d['r2'] - 1, d['r3'] - 1 
                                d['Root Indices'] = root_indices
                                combinations.append(d)
        return combinations



def copy_to_clipboard(text):  #OSX only: Copy text to buffer.
    subprocess.run('pbcopy', universal_newlines=True, input=text)


if __name__ == "__main__":
    #Create all possible indices combinations for root.
    #!pip install pandas
    #!pip install tabulate
    from numpy import array as _A
    import subprocess

    self = RootPredictor()
    combinations = list()  #_A(self.generate_all_combinations())
    PREFIX_HE = "ה, מ, א, ת, י, ת, נ, ני, הו, יו, תו, נו, או, לו, לי, הת, נת, ית, ו,".replace(' ', '').split(',')
    SUFFIX_HE = "תי, תם, תן, נו, ן, ונה, ה, ים, ות, נה, ת, י,".replace(' ', '').split(',')

    HE_INFIX_I1 = ['י', '' , 'ו']
    HE_INFIX_I1 = ['']
    HE_INFIX_I2 = ['']
    HE_SUFFIX= 'תי,תם,תן,נו,ן,ונה,ה,ים,ות,נה,ת,י,'.replace(' ', '').split(',')
    HE_ROOTS3 = [root.strip() for root in ROOTS_HE_3_LETTERS.open('rt').readlines()]

    combinations = list()

    for P in PREFIX_HE:
        for R1 in HE_ROOTS3[0]:
            for I1 in HE_INFIX_I1:
                for R2 in HE_ROOTS3[1]:
                    for I2 in HE_INFIX_I2:
                        for R3 in HE_ROOTS3[2]:
                            for S in HE_SUFFIX:
                                word = ''.join((P, R1, I1, R2, I2, R3, S))
                                #word = ''.join((S, R3, I2, R2, I1, R1, P))
                                combinations.append(dict(
                                    word=word,
                                    root= (R1, R2, R3),
                                    P=P, R1=R1, I1=I1, R2=R2, I2=I2, R3=R3, S=S
                                ))

    words_only = [combination['word'] for combination in combinations]
    with _P(ROOT_FOLDER / "words_only.txt").open('wt') as f:
        for word in words_only: 
            f.write(word+"\n")
    #os.system(f"code '{ROOT_FOLDER}/words_only.txt'")

    words_only = [(combination['word'], ''.join(combination['root'])) for combination in combinations]
    with _P(ROOT_FOLDER / "words_and_roots.txt").open('wt') as f:
        for word in words_only: 
            f.write(f"{word}\n")
    os.system(f"code '{ROOT_FOLDER}/words_and_roots.txt'")

    json.dump(combinations, (ROOT_FOLDER / "synth3.json").open('wt'), ensure_ascii=False)

    simple = [line['word'] for line in combinations]
    json.dump(simple, (ROOT_FOLDER / "synth3_simple.json").open('wt'), ensure_ascii=False)
    #os.system(f"code {ROOT_FOLDER / 'synth3_simple.json'}")

    print(f"Found Total of {len(combinations)} combinations.")

    for i, combination in enumerate(combinations):
        print(f"{i:4}\t{combination}")
        break


