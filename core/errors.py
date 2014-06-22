'''Some basic errors I like'''

class CatchMe(Exception):
    '''Throw manually to force something to rollback before continuing.'''
    pass

class Base(Exception):
    def __new__(cls, class_, val, method, message):
        self = super(Base, cls).__new__(message)
        self.method = method
        self.cls = class_
        self.val = val
        return self
        
