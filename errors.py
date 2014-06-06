
class Base(Exception):
    def __new__(cls, class_, val, method, message):
        self = super(Base, cls).__new__(message)
        self.method = method
        self.cls = class_
        self.val = val
        return self
        
