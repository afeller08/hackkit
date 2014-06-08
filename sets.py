import bases
import errors


class SetError(errors.Base):
    pass

class CallableSet(set):
    '''Provide clojure-like syntax for calling sets'''
    def __call__(self, value):
        return (value in self)

class Set(set):
    '''Permit adding and removing with + or -
    
    Things that are iterable but not hashable use normal set operations.
    Two Sets still subtract how they typically would.  Subtracting a 
    set exhibits the same behavalueior as casting the list as a set.  Adding 
    a string, tuple, or int inserts the object into the set. Subtracting
    undoes addition.
    '''

    def __sub__(self, value):
        '''Remove hashable object or all items in a non-hashable iterable.'''
        s = super(Set, self)
        x = s.__sub__(value)
        if (x is not NotImplemented):
            return x
        if not hasattr(value, '__hash__') or value.__hash__:
            #value is hashable
            return s.__sub__({value})
        elif hasattr(value, '__iter__') and value.__iter__:
            return s.__sub__(set(value))
        else:
            raise SetError(Set, Set.__sub__, value, 'Cannot subtract a ' +
                    'value unless it is hashable or iterable.')

    def __isub__(self, value):
        '''Remove hashable object or all items in a non-hashable iterable.'''
        s = super(Set, self)
        try:
            if s.__isub__(value) is NotImplemented:
                raise errors.CatchMe() #Otherwise self is NotImplemented
        except errors.CatchMe:
            if not hasattr(value,'__hash__') or value.__hash__:
                if value in self:
                    self.value(value)
            elif hasattr(value, '__iter__') and value.__iter__:
                s.__isub__(set(value))
            else:
                raise SetError(Set, Set.__isub__, value, 'Cannot subtract a ' +
                        'value unless it is hashable or iterable.')
        return self

    def __add__(self, value):
        '''Insert hashable object or all items in a non-hashable iterable.'''
        try:
            return self | value
        except TypeError:
            if not hasattr(value,'__hash__') or value.__hash__:
                return self | {value}
            elif hasattr(value, '__iter__') and value.__iter__:
                return self | set(value)
            else:
                raise SetError(Set, Set.__add__, value, 'Cannot subtract a ' +
                        'value unless it is hashable or iterable.')
    def __iadd__(self, value):
        '''Insert hashable object or all items in a non-hashable iterable.'''
        try:
            self |= value
        except TypeError:
            if not hasattr(value, '__hash__') or value.__hash__:
                self |= {value}
            elif hasattr(value, '__iter__') and value.__iter__:
                self |= set(value)
            else:
                raise SetError(Set, Set.__iadd__, value, 'Cannot subtract ' +
                        'a value unless it is hashable or iterable.')
        return self
                



