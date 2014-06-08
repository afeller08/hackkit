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

import inspect
import common

class ArgInfo():
    @attributes
    def __init__(self, args, defaults, varargs=None, keywords=None):
            pass

def arginfo(function, _ugly=False):
    try:
        argspec = inspect.getargspec(function)
    except:
        return None
    vars = common.deindex(argspec.args)


def factory(function, registry, **aliases):

