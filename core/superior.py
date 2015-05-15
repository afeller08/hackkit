'''Implement a proxy for super that can be operated on.

I find the following syntax cumbersome:
class Word(str):
    def __add__(self, other):
        return super(Word, self).__add__(' ' + other)

I'm implemting am alternative such that

superior.super(Word, self) + whatever

is valid code.  It is intended tp be used with the kind of decorators
found in the registry so that the following sentax would be supported.

@superior.subclass
class Subclass(Base):
    def __add__(self, super, other):
        return  super + Subclass(other)
    def __imul__(self, superior, other):
        superior *= Subclass(other)
        return self
    def __sub__(self, other):
        return self.something_inherited - self.preprocess(other)
'''
import inspect
from hackkit.helpers import common


def enable_proxy(attr):
    '''If attr is a method, transform its first argument to arg.proxy.

    Used as a decorator for methods in proxy objects.
    '''
    if not callable(attr):
        return attr

    def proxy_method(self, *args, **kwargs):
        return attr(self.proxy, *args, **kwargs)

    return proxy_method


def _MakeProxy(name, bases, dict, type=type):
    '''Create the new proxy for super. Use as a metaclass.'''
    # cls is the object's class. class_ is the method's class.
    # If they are not equal, cls is a superclass of class_.
    cls = dict['cls']
    class_ = dict['class_']
    source = super(class_, cls)
    d = {'__metaclass__': _MakeProxy}
    # __getattribute__ and subclassing dict don't work.
    for attr in class_.__dict__:
        try:
            d[attr] = enable_proxy(getattr(source, attr))
        except AttributeError:
            pass
    return type(name, bases, d)


_memoizations = {}


def superproxy(class_, instance, memoize=True):
    '''Delegate and memoize the creation of the super proxy'''
    cls = instance.__class__
    description = (class_, cls)  # Needed for SuperProxy
    Proxy = None
    if memoize:
        try:
            Proxy = _memoizations[description]
        except KeyError:
            pass
    if Proxy is None:

        # Create one class per (subclass, superclass) pair
        class SuperProxy(object):
            __metaclass__ = _MakeProxy
            class_ = description[0]
            cls = description[1]

        Proxy = SuperProxy
        if memoize:
            _memoizations[description] = Proxy
    proxy = Proxy()
    proxy.proxy = instance
    return proxy


def _wrapself(method, name, cls, position, memoize):
    '''Decorate method to have super(cls, self) at position.'''
    start = position
    position = max(position, 1)

    def wrapper(*args, **kwargs):
        self = args[0]
        proxy = superproxy(cls, self, memoize)
        args = args[:start] + (proxy,) + args[position:]
        return method(*args, **kwargs)
    wrapper.__name__ = name
    return wrapper


def _wrapmethod(method, attr, cls, position):
    '''Decorate method to have super(cls, self).attr at position.'''
    start = position
    position = max(position, 1)

    def wrapper(*args, **kwargs):
        self = args[0]
        proxy = super(cls, self)
        proxymethod = getattr(proxy, attr)
        args = args[:start] + (proxymethod,) + args[position:]
        return method(*args, **kwargs)
    wrapper.__name__ = attr
    return wrapper


def subclass(cls, memoize=True):
    for attr in vars(cls):
        method = getattr(cls, attr)
        if callable(method):
            argspec = common.deindex(inspect.getargspec(method).args)
            index = 0
            if hasattr(method, 'im_func'):
                method = method.im_func
            if 'superior' in argspec:
                index = argspec['superior']
                method = _wrapself(method, attr, cls, index, memoize)
            if 'sup' in argspec:
                index = argspec['sup']
                method = _wrapmethod(method, attr, cls, index)
            setattr(cls, attr, method)
    return cls

TESTING = True
if TESTING:
    @subclass
    class Test(int):
        def __add__(self, sup, other):
            # Have to cast because ints are primative and
            # don't update their subclasses.
            return Test(sup(other + 1))

        def __sub__(superior, other):
            return superior - (other + 1)

    t = Test(3) + 3
    if t == 7:
        print 'sup works'
    t = Test(7) - 3
    if t == 3:
        print 'superior works'
    if (Test(9) - 4) == 4:
        print 'memoization doesnt break it'
