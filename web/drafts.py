import inspect
import json


from hackkit.helpers import common


registry = None


def jsonp_handler(function, namespace=''):
    '''Create a javascript function that will call this one over ajax.'''
    args = inspect.getargspec(function)
    name = function.__name__
    names = args.args
    places = common.deindex(names)
    argcount = len(places)
    defaults = args.defaults or []
    argcount -= len(defaults)
    variable = args.varargs
    if variable:
        argcount -= 1
    keywords = args.keywords or (variable and defaults)
    args = argcount * [None]
    if not variable:
        args += defaults

    def handler(data, id):
        data = json.loads(data)  # Or let the registry take care of it
        if not (variable or keywords):
            return function(*args)
    handler.__name__ = name + '_handler'
    registry.register(handler)
    return function
