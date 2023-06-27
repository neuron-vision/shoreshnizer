'''
Author: Ishay Tubi, Neuron Vision
Date: June 14, 2023
Description: 
python class for nicer code completion
'''

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

