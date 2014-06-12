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
from collections import namedtuple
import inspect

import common

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


def factory(function, registry, **aliases):
    pass


def attributes(function):
    '''Set args[1:] as attributes of args[0].

    Used primarily for __init__.
    '''
    mymy = arginfo()



