'''
Author: Ishay Tubi, Neuron Vision
Date: June 14, 2023
Description: Utility functions for clustering characters.
'''
from pathlib import Path as _P
import os
from typing import Tuple, List
from rootenizer.word_break_down import WordBreakDown


def character_index(char:str)->int:
    ''' 
    Translate a single character to character index in alphabet.
    '''

    o = ord(char)
    if ord('א')<= o <= ord('ת'):
        return o - ord('א')
    elif ord('a')<= o <= ord('z'):
        return o - ord('a')
    else:
        return o  # Return ascii index value for unknown chars.


def remove_characters(string:str, indices:list):
    '''
    Return only the characters that are not in indices 
    '''
    return ''.join([char for idx, char in enumerate(string) if idx not in indices])



_sofiot_to_middle_translation = {
    'ף':'פ',
    'ך':'כ',
    'ם':'מ',
    'ן':'נ',
    'ץ':'צ',    
}

def convert_sofiot_to_middle(word):
    '''
    Convert אותיות סופיות to אותיות אמצעיות so we can generalize the roots
    '''
    return ''.join([_sofiot_to_middle_translation.get(ot, ot) for ot in word])
