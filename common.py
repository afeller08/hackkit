'''Some core utilities I routinely use.'''

def attr(obj, attribute):
    return object.__getattribute__(obj, attribute)

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

    def __init__(self, base=None, previous=False, args=None, method=None):
        self.chain = ()
        if previous:
            base = attr(previous, 'base')
            chain = attr(previous, 'chain')
            self.chain = ((args, method),) + chain
        self.base = base

    def __getitem__(self, item):
        return Accessor(self, None, item, Accessor.ITEM)

    def __getattribute__(self, attr):
        return Accessor(self, None, Accessor.ATTR)

    def __call__(self, *args, **kwargs):
        return Accessor(self, None, (args, kwargs), Accessor.CALL)

    def access(self, obj=None):
        chain = attr(self, 'chain')
        if obj is None:
            obj = attr(self, 'base')
        for (item, method) in chain:
            if method == Accessor.ITEM:
                obj = obj[item]
            if method == Accessor.ATTR:
                obj = getattr(obj, item)
            if method == Accessor.CALL:
                (args, kwargs) = item
                obj = obj(*args, **kwargs)
        return obj

class MRCA():
    __metaclass__ = type
    # TODO: need to override isinstance and issubclass and provide joining
    # mechanisms.


def mcra(*objects_or_classes):
    '''Return most recent common ancestor (MCRA) of the inputs.
    
    Given Python's support of complex inheritance patterns, this is
    technically an NP-complete problem (longest common substring on n
    input strings).

    I seek to produce an implementation that is efficient in the common
    case while remaining correct in the complex case.

    ...needs more thought

    This implementation seeks to produce a 
    '''
    def init(self, object_or_class):
        cls = object_or_class
        if not isinstance(cls, type):
            cls = cls.__class__
        c = obj_or_cls
        if not isinstance(c, type):
            c = c.__class__

