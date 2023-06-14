
from pathlib import Path as _P
import os
from typing import Tuple, List
from word_break_down import WordBreakDown


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

