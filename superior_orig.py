''' Implements a decorator for improving the syntax of super.

I find the following syntax hard to read:
class Word(str):
    def __add__(self, other):
        return super(Word, self).__add__(' ' + other)

I'd much rather use:
@superior.super
class Word(str):
    def __add__(self, other):
        return self.super[Word] + (' ' + other)

We need to use getitem instead of a function call, because assigning to
a function call is invalid.  super is, in my opinion, deficient at
dealing with in place operations due to handling of NotImplemented.
If I'm improving super, I especially want to support things like

self.super[Word] += ' ' + other

I wrote this handler to support the second kind of syntax.
'''

# N.B.  This file is not meant to serve as a reference for what good code
# should look like.  I wrote it because I wanted to make other code more
# readable.  I expect to use it more often than I use any other module
# I've ever written because it kills what has always been my biggest
# annoyance with Python.  The only circumstance under which I ever expect
# to edit this file is to improve memoization, or make it Python3
# compatible.

import weakref

def _TCCMetaclass(name, bases, dict):
    '''Create the new super proxy'''
    object = dict['object']
    class_ = dict['class_']
    d = {}
    # __getattribute__ and subclassing dict don't work.
    for attr in class_.__dict__:
        try:
            d[attr] = getattr(super(class_, object), attr)
        except AttributeError:
            pass
    return type(name, bases, d)

    
class _SuperDelegator(object):
    '''Delegate and memoize the creation of the super proxy'''
    memory = {}
    
    def __init__(self, object, memoize=True):
        self.object = object
        self.memoize = memoize

    def __getitem__(self, class_):
        '''Delegate the creation of the super proxy'''
        memoize = self.memoize
        instance = (class_, self.object)
        if memoize:
            try:
                return _SuperDelegator.memory[instance]
            except KeyError:
                pass

        # Create one class per instance
        class TightlyCoupledClass(object):
            __metaclass__ = _TCCMetaclass
            class_ = instance[0] 
            object = instance[1]

        attribute = TightlyCoupledClass()
        if memoize:
            _SuperDelegator.memory[instance] = weakref.ref(attribute)
        return attribute

    

def superior(cls, memoize=True):
    '''Add attribute super to a class.
    Optional parameter to turn off memoization.
    '''
    def init(self, *args):
        val = super(cls, self).__init__(*args)
        self.super = _SuperDelegator(self, memoize)
        return val

    cls.__init__  = init
    return cls


TESTING = True
if TESTING:
    @superior
    class Test(int):
        def __add__(self, other):
            # Have to cast because ints are primative and
            # don't update their subclasses.
            return Test(self.super[Test] + (other + 1))
        def __iadd__(self, other):
            self.super[Test] += other
            return self

    t = Test(3) + 3 
    x = 3 + Test(3)
    print x
    #t += 1
    if t == 10:
        print 'It works!'
