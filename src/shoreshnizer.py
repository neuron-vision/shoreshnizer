'''
הרצת המחלקה מאפשרת לקבל מילה או אוסף מילים לקבל ייצוג טוקנים משמר סמנטיקה
'''

from typing import Any
from pathlib import Path as _P
import os
import json


def remove_characters(string:str, indices:list):
    '''
    Return only the characters that are not in indices 
    '''
    return ''.join([char for idx, char in enumerate(string) if idx not in indices])


class Shoreshnizer(object):
    '''
    Predict the root of each root and cluster all the rest of the charcaters.
    '''
    def __init__(self, voc_path:str=None) -> None:
        self.voc_path = _P(voc_path or 'resurces/voc.json')
        self.shoresh_list = json.load(self.voc_path.open('rt'))
        print(f"Loaded {len(self.shoresh_list)} words with roots.")
    
    def predict_shoresh(self, word:str):
        '''
        Return the index of root letters.
        Shorsh start,
        Shoresh end,
        '''
        word = word.strip()  # Remove blanks
        if word in self.shoresh_list:
            shoresh, idx = self.shoresh_list[word]
            return shoresh, idx
        
        #Fallback 1: Apply fuzzy logic
        #Fallback 2: Select all as root for short words.
        #Fallback 3: Use char based?
        
        # Not found, use fallback, the whole word is a shoresh?
        return word, range(len(word))



    def process_words(self, word):
         shoresh, idx = self.predict_shoresh(word)
         start, stop = idx[0], idx[-1]
         prefix = word[:start]  if start>0 else '' # Slice what ever starts before the shoresh
         suffix = word[stop+1:]  # Slice what ever ends after the shoresh
         no_suffix = word[:stop+1]
         middle = remove_characters(no_suffix, idx)[start:]  # Remove the shoresh and keep only what is left in the middle.
         return dict(
             tokens=dict(
                prefix=prefix,
                shoresh=shoresh,
                middle=middle,
                suffix=suffix
             ),
             shoresh_start=start,
             shoresh_stop=stop,
         )

    def __call__(self, sentence:str) -> Any:
        words = sentence.split()
        breakdowns = []  # return value
        for word in words:
            breakdowns.append(self.process_words(word))
        return breakdowns
    
    def html(self, list_of_breakdowns):
        '''
        Utility to dump tokens with html colors
        '''
        css = "<style> \
                .shoresh {background-color: yellow;} \n\
                .prefix  {background-color: green;} \n\
                .middle {background-color: orange;} \n\
                .suffix {background-color: red;} \n\
                </style>"
        html = '' + css
        for breakdown in list_of_breakdowns:
            tokens = breakdown['tokens']
            message = \
                "<span class=prefix>{prefix}</span> \
                <span class=shoresh>{shoresh}</span> \
                <span class=middle>{middle}</span> \
                <span class=suffix>{suffix}</span>".format(**tokens)

            html = html + "</br>" + message
        return html
    
    def train(self):
        '''
        Minimize recunstruction error, Show the error is minized as a factor of the 
        '''
        raise BaseException("מימוש חסר")
    
    def stats(self):
        '''
        plot algorithm statistics for research.
        '''

if __name__ == '__main__':
    voc_path = 'src/mini_shoreshnizer.json'
    self = Shoreshnizer(voc_path=voc_path)
    sentance = 'אם נסתכל על המשפט הזה נצליח להתבונן על מיקרי הקצה'
    sentance = "נסתכל להתבונן אוניברסיטה"
    list_of_breakdowns = self(sentance)
    html = self.html(list_of_breakdowns)
    sample_path = 'samples/1.html'
    _P(sample_path).open('wt').write(html)
    print(f"Samples is saved to {sample_path}")
    os.system(f'open {sample_path}') # Works on OSX only
    print(list_of_breakdowns)

