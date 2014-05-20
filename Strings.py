import Bases
import string
import Sets

class Set(Sets.Set):
    pass

class Object(Bases.Object):
    pass


class CursoryGlance(Object):
    '''
    A CursoryGlance lets you detect very basic information about a string.
    '''
    def __init__(self, punctChars=None):
        '''
        punctChars is a function returning whether the argument to it should
        be treated as a deliniation character or a word.
        It may also be an iterable that can be turned into a set in which case
        it will be turned into a function for containment.
        '''
        if punctChars == None:
            s = string
            punctChars = Set(s.whitespace + s.punctuation) - '_'
        if not hasattr('__call__', punctChars):
            punctChars = Set(punctChars)
        self.isPunctChar = punctChars
