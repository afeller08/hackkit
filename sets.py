import Bases
import Exceptions



class SetException(Exceptions.Base):
    pass

class Set(set):

    def __call__(s,v):
        return (v in s)

    def __sub__(s,v):
        s = super(Set,s)
        x = s.__sub__(v)
        if (x != NotImplemented):
            return x
        if not hasattr(v, '__hash__') or v.__hash__:
            #v is hashable
            return s.__sub__({v})
        elif hasattr(v, '__iter__') and v.__iter__:
            return s.__sub__(set(v))
        else:
            raise SetException(Set, Set.__sub__, v, 'Cannot subtract a ' +
                    'value unless it is hashable or iterable.')

    def __isub__(self,v):
        s = super(Set,self)
        try:
            if s.__isub__(v) == NotImplemented: raise Exception()
        except:
            if not hasattr(v,'__hash__') or v.__hash__:
                if v in self:
                    self.remove(v)
            elif hasattr(v, '__iter__') and v.__iter__:
                s.__isub__(set(v))
            else:
                raise SetException(Set, Set.__isub__, v, 'Cannot subtract a ' +
                        'value unless it is hashable or iterable.')
        return self

    def __add__(s,v):
        try:
            return s | v
        except:
            if not hasattr(v,'__hash__') or v.__hash__:
                return s| {v}
            elif hasattr(v, '__iter__') and v.__iter__:
                return s | set(v)
            else:
                raise SetException(Set, Set.__add__, v, 'Cannot subtract a ' +
                        'value unless it is hashable or iterable.')
    def __iadd__(s,v):
        try:
            s |= v
        except:
            if not hasattr(v,'__hash__') or v.__hash__:
                s |= {v}
            elif hasattr(v, '__iter__') and v.__iter__:
                s |= set(v)
            else:
                raise SetException(Set, Set.__iadd__, v, 'Cannot subtract a ' +
                        'value unless it is hashable or iterable.')
        return s
                



