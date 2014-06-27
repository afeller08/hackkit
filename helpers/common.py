'''Some core utilities I routinely use.'''
import weakref


def subsets(iterable, n):
    iterable = list(iterable)
    if n > len(iterable):
        return []
    if n == 1:
        return [(x,) for x in iterable]


def _subsets(iterable, n):
    return


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
        return self.__class__(self, None, item, Accessor.ITEM)

    def __getattribute__(self, attr):
        return self.__class__(self, None, Accessor.ATTR)

    def __call__(self, *args, **kwargs):
        return self.__class__(self, None, (args, kwargs), Accessor.CALL)

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


class _MRCA_Metaclass(type):
    def __isinstance__(MRCA, obj):
        return MRCA.__issubclass__(obj.__class__)

    def __issubclass__(MRCA, cls):
        if cls in MRCA.known_subclasses:
            return True
        mro = deindex(cls.__mro__)
        for base in MRCA.bases:
            if base not in mro:
                return False
        for (a, b) in MRCA.basepairs:
            if mro[b] < mro[a]:
                return False
        MRCA.known_subclasses.add(weakref.ref(cls))
        return True


def mrca(object_or_class, *objects_or_classes):
    '''Return most recent common ancestor (MRCA) of the inputs.'''
    '''
    Given Python's support of complex inheritance patterns, the obvious
    approach involves solving an NP-complete problem.
        (Longest common substring on n input strings)

    I seek to produce an implementation that is efficient in the common
    case while remaining correct in the complex case.

    The biggest efficiency we can gain in the common case is memoization
    on class.  Very rarely would we test a type against an MRCA only
    once.  Such uses are likely to be very slow.

    One other thing to note is that the mor in python only permits each
    superclass to show up once in a class's hierarchy.  This allows us
    to create a complete description of the string simply through pairs
    (so we are no longer dealing with an NP-complete problem.)
    '''
    mrca = object_or_class
    if not isinstance(mrca, type):
        mrca = mrca.__class__
    for cls in objects_or_classes:
        if not isinstance(cls, type):
            cls = cls.__class__
        if not issubclass(cls, mrca):
            if not issubclass(mrca, cls):
                mrca = _createmrca(mrca, cls)
    return mrca


def _createmrca(cls1, cls2, memoize=True):
    saved = _createmrca.mrcas.get
    cls = saved((cls1, cls2)) or saved((cls2, cls1))
    if cls is not None:
        return cls
    bases = None
    basepairs = None
    if hasattr(cls1, '_hackkit_MRCA__MRCA'):
        bases = cls1.bases
        basepairs = set(cls1.basepairs)
    else:
        bases = set(cls1.__mro__)
    if hasattr(cls2, '_hackkit_MRCA__MRCA'):
        bases &= cls2.bases
        if basepairs:
            basepairs &= cls2.basepairs
    else:
        bases &= set(cls2.__mro__)
        if basepairs:
            source = deindex(cls2.__mro__)
            for (a, b) in basepairs:
                aa = source.get(a)
                bb = source.get(b)
                if aa is None or bb is None or bb < aa:
                    basepairs.remove((a, b))
    if basepairs is None:
        basepairs = set()
        bps = subsets(bases, 2)
        mro1 = deindex(cls1.__mro__)
        mro2 = deindex(cls2.__mro__)
        for (a, b) in bps:
            a1 = mro1[a]
            b1 = mro1[b]
            a2 = mro2[a]
            b2 = mro2[b]
            if (a1 < b1 and a2 < b2) or (b1 < a1 and b2 < a2):
                basepairs.add((a, b))

    class MRCA(type):
        known_subclasses = set()
        __metaclass__ = _MRCA_Metaclass
        _hackkit_MRCA__MRCA = True
    MRCA.bases = bases
    MRCA.basepairs = basepairs
    return MRCA


_createmrca.mrcas = {}
