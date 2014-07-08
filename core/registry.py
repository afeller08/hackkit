'''Store decorators for argument feeding.

Python gives you a lot of freedom to manipulate and extend the
language.  I've recently become emamored with the concept of
requesting information by name in function calls.  To me, its the
logical next step from duck typing.  The most obvious examples are in
UI, events have a lot of properties, but I'm usually interested in a
very small subset of them in any given function.

What I want to be able to do is write:

@registry.event
def cursorMoved(x_pos, y_pos):
    ...

in one module, and

@registry.event
def cursorMoved(line, char_index):
    ...


in another, and have the correct arguments pulled out of the event
and passed to my function.  Ideally, the resulting function will be
able to be called either with the arguments specified or with just
the event.
'''
from collections import namedtuple, defaultdict
import inspect

import common


def combine_metaclasses(*metaclasses):
    '''Chain metaclasses that take a type=type fourth argument.

    '''
    args = metaclasses
    metaclass = metaclasses[-1]
    metaclasses = list(metaclasses[:-1])
    metaclasses.reverse()
    for func in metaclasses:
        # Define metaclass recursively.
        def metaclass(name, bases, dict, metaclass=metaclass):
            return func(name, bases, dict, metaclass)
    metaclass.__doc__ = 'Combined metaclasses of {0}.'.format(args)
    return metaclass


ArgInfo = namedtuple(
    'ArgInfo',
    ['args', 'defaults', 'varargs', 'keywords']
)


def arginfo(function):
    try:
        argspec = inspect.getargspec(function)
    except:
        return None
    args = common.deindex(argspec.args)
    defaults = argspec.defaults
    defaults = [common.ignore] * (len(args) - len(defaults)) + defaults
    defaults = common.maponto(args, defaults)
    return ArgInfo(args, defaults, argspec.varargs, argspec.keywords)


class Registry(type):
    '''
    Typically, you use in the following manner:

    class MyRegistry(Registry):
        pass

    I want to have the syntax in example registry available

    ... needs some more thought
    '''
    BaseClass = None


class ExampleRegistry(Registry.BaseClass):
    def classHandling(self, whatever):
        pass


class oldRegistry(object):
    records_functions = True
    records_classes = False
    registries = defaultdict(lambda: {})

    def __init__(self, **kwargs):
        self.values = self.registries('values')
        self.register(**kwargs)
        if self.records_classes:
            self.classes = self.registries('classes')
        if self.records_functions:
            self.functions = self.registries('functions')
            self.arguments = self.registries('arguments')
        return

    def _values(self, key, value):
        self.values[key] = value
        return

    def register(self, **kwargs):
        '''Create value in registry'''
        for key, v in kwargs.iteritems():
            if isinstance(v, common.Accessor):
                self._values(key, lambda v=v: common.Accessor.access(v))
            elif callable(v):
                self._values(key, v)
            else:
                self._values(key, lambda v=v: v)
        return

    def __call__(self, method_or_cls):
        if isinstance(self, type):
            return self.decorate_cls(method_or_cls)
        return self.decorate_method(method_or_cls)

    def decorate_cls(self, cls, name=None):
        if self.records_classes:
            if name is None:
                name = cls.__name__
            self.classes[name] = cls
        for attr, method in vars(cls).iteritems():
            if callable(method):
                method = self.decorate_method(method, cls)
                setattr(cls, attr, method)
        return cls

    def decorate_method(self, method, name=None, cls=None):
        args = arginfo(method)
        if 'cls' in args.args:
            method._hackkit_registry__cls = cls
        if self.records_functions and cls is None:
            if name is None:
                name = method.__name__
            self.functions[name] = method
            self.arguments[name] = args

        def function(*args, **kwargs):
            pass
        return function


def attributes(function):
    '''Set args[1:] as attributes of args[0].

    Used primarily for __init__.
    '''
    mymy = arginfo()
    return mymy
