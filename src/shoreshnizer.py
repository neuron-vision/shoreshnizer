'''
Running this class allows receiving a word or a collection of words to obtain a representation of tokens that preserves semantic meaning.
'''

from pathlib import Path as _P
import os
import json
from typing import Tuple, List


def remove_characters(string:str, indices:list):
    '''
    Return only the characters that are not in indices 
    '''
    return ''.join([char for idx, char in enumerate(string) if idx not in indices])

class WordBreakDown(object):
    '''
    Use a python class for word break down instead of a dictionary to allow code completion.
    '''
    def __init__(self, prefix, root, infix, suffix):
        self.prefix = prefix
        self.root = root
        self.infix = infix
        self.suffix = suffix

    def __str__(self):
        return f"<{self.prefix}><{self.root}><{self.infix}><{self.suffix}>"
    
    def __repr__(self) -> str:
        return self.__str__()

class Shoreshnizer(object):
    '''
    Predict the root of each root and cluster all the rest of the characters.
    '''
    def __init__(self, voc_path:str=None) -> None:
        self.voc_path = _P(voc_path or 'resources/voc.json')
        self.shoresh_list = json.load(self.voc_path.open('rt'))
        print(f"Loaded {len(self.shoresh_list)} words with roots.")

        # Hardcoded params to be moved out to configuration file later:
        self.total_number_of_bits_per_word = 32  
        self.number_of_bits = dict(
            root = 5,  # Number of bits used for a single root char.
            infix = 2,
            prefix = 4,
            suffix = 4,
            other = 7  # Special chars
        )
    
    def predict_shoresh(self, word:str):
        '''
        Return the index of root letters.
        Shoresh start,
        Shoresh end,
        '''
        word = word.strip()  # Remove blanks
        if word in self.shoresh_list:
            root, idx = self.shoresh_list[word]
            return root, idx
        
        #Fallback 1: Apply fuzzy logic
        #Fallback 2: Select all as root for short words.
        #Fallback 3: Use char based?
        
        # Not found, use fallback, the whole word is a root?
        return word, range(len(word))


    def character_index(self, char:str)->int:
        o = ord(char)
        if ord('א')<= o <= ord('ת'):
            return o - ord('א')
        elif ord('a')<= o <= ord('z'):
            return o - ord('a')
        else:
            return o  # Return ascii index value for unknown chars.

    def embed(self, breakdown:WordBreakDown):
        '''
        Convert a breakdown dict into a 32 unsigned integer.
        '''
        # Start with root chars.
        embedding = 0
        root_bit_mask = (2**self.number_of_bits['root'] -1)
        for i, char in enumerate(breakdown.root):
            char_index = self.character_index(char) + 1  # Preserve 0 for no value, start with 1 for exiting value.
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
        suffix_val = sum([char-'א' for char in breakdown.suffix])
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


    def process_word(self, word) -> WordBreakDown:
         '''
         Process single word: Predict the root, assign all other chars with their locations.

         '''
         root, idx = self.predict_shoresh(word)
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


    def __call__(self, sentence:str) -> Tuple[List[int], List[WordBreakDown]]:
        ''' 
        Input: A sentence with multiple words separated with spaces.
        Output: List of dictionary breakdown per word.
        '''
        words = sentence.split()
        breakdowns_list = []  # The returning value
        embedding_list = []
        for word in words:
            breakdown = self.process_word(word)
            breakdowns_list.append(breakdown)

            embedding = self.embed(breakdown)
            embedding_list.append(embedding)
        return embedding_list, breakdowns_list
    
    def html(self, list_of_breakdowns) ->str:
        '''
        Utility to dump tokens with html colors
        '''
        css = "<style> \n \
                .root {background-color: yellow;} \n\
                .prefix  {background-color: green;} \n\
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
    voc_path = 'src/mini_shoreshnizer.json'
    self = Shoreshnizer(voc_path=voc_path)
    sentence = 'אם נסתכל על המשפט הזה נצליח להתבונן על מיקרי הקצה'
    sentence = "נסתכל להתבונן אוניברסיטה"
    embedding_list, breakdowns_list = self(sentence)
    print("embedding_list")
    print(embedding_list)
    html = self.html(breakdowns_list)
    sample_path = 'samples/1.html'
    _P(sample_path).open('wt').write(html)
    print(f"Samples is saved to {sample_path}")
    os.system(f'open {sample_path}') # Works on OSX only
    print(breakdowns_list)

