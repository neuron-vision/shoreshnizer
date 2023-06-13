'''
הרצת המחלקה מאפשרת לקבל מילה או אוסף מילים לקבל ייצוג טוקנים משמר סמנטיקה
'''

from typing import Any


class Shoreshnizer(object):
    '''
    '''
    def __init__(self, voc_path:str=None) -> None:
        self.voc_path = voc_path or 'resurces/voc.json'
    
    def predict_shoresh(self, word):
        '''
        Return the index root and index of:
        Shorsh start,
        Shoresh end,
        '''
        # For testing return 1,2,3 always if len is 3 and above.
        if len(word)<3:
            return word, (0, 1)
        elif len(word)<4:
            return word, (0, 2)
        else:
            return word, (1, 3)


    def process_words(self, word):
         shoresh, (start, stop) = self.predict_shoresh(word)
         prefix = word[:start]  # Slice what ever starts before the shoresh
         suffix = word[stop:]  # Slice what ever ends after the shoresh
         middle = word[start:stop].replace(shoresh, '')  # Remove the shoresh and keep only what is left in the middle.
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
    
    def train(self):
        raise BaseException("מימוש חסר")
    
    def stats(self):
        '''
        plot algorithm statistics for research.
        '''

if __name__ == '__main__':
    self = Shoreshnizer()
    sentance = 'אם נסתכל על המשפט הזה נצליח להתבונן על מיקרי הקצה'
    tokens = self(sentance)
    print(tokens)

