'''Some core utilities I routinely use.'''

def deindex(iterable):
    '''Return a dict mapping the values to the keys of the iterable.'''
    result = {}
    if isinstance(iterable, dict):
        iterable = iterable.iteritems()
    for i, value in enumerate(iterable):
        result[value] = i
    return result 

class Accessor(object):
    CALL = 0
    ATTR = 1
    ITEM = 2
    '''A proxy object to traverse another object

    >>> accessor = Accessor():
    >>> accessor = accessor(some, args)
    >>> accessor = accessor[item]()
    >>> accessor = accessor.attr.reference[3]

    >>> Accessor.access(accessor, obj)
    returns the value of
      obj(some, args)[item]().attr.reference[3]
    '''

    def __init__(self, previous=False, args=None, method=None):
        self.chain = ()
        if previous:
            chain = object.__getattr__(previous, 'chain')
            self.chain = ((args, method),) + chain

    def __getitem__(self, item):
        return Accessor(self, item, Accessor.ITEM)

    def __getattr__(self, attr):
        return Accessor(self, attr, Accessor.ATTR)

    def __call__(self, *args, **kwargs):
        return Accessor(self, (args, kwargs), Accessor.CALL)

    def access(self, obj):
        chain = object.__getattr__(self, 'chain')
        for (item, method) in chain:
            if method == Accessor.ITEM:
                obj = obj[item]
            if method == Accessor.ATTR:
                obj = getattr(obj, item)
            if method == Accessor.CALL:
                (args, kwargs) = item
                obj = obj(*args, **kwargs)
        return obj

