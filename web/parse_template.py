_templates = {}


def case(func, char):
    '''Extend parse_template by using @case('c').

    The decorated function creates a template for c`...`.
    c may be any character.
    '''
    _templates[char] = func
    return func


def jsformat(object):
    if hasattr(object, 'jsformat'):
        return object.jsformat()
    elif isinstance(object, (float, int, str)):
        return repr(object)
    elif isinstance(object, unicode):
        return repr(object)[1:]
    elif isinstance(object, (set, list, tuple)):
        list = [jsformat(obj) for obj in object]
        list[0] = '[' + list[0]
        list[-1] += ']'
        return ', '.join(list)
    elif isinstance(object, dict):
        # can probably be done better at least for the key.
        dict = [(jsformat(a), jsformat(b)) for (a, b) in object.iteritems()]
        dict = ['{0}: {1}'.format(a, b) for (a, b) in dict]
        return ', '.join(dict)


@case('`')
def _backtick(template, context, i):
    char = ''
    out = []
    while char != '`':
        out.append(char)
        char = template[i]
        i += 1
    out = ''.join(out)
    out = jsformat(context[out])
    return (out, i)


@case('(')
def _paren(template, context, i):
    params = _gather(template, context, i, ')')
    out = ['(']
    for x in params:
        if not isinstance(x, basestring):
            raise TypeError("_paren requires strings. TODO: better error")
        out.append(x)
    out.append(')')
    return ''.join(out)


def is_ntuple(thing, n):
    if isinstance(thing, tuple) and len(thing) == n:
        return True
    return False


@case('{')
def _curly(template, context, i, indent=0):
    keys_values = _gather(template, context, i, ')')
    if isinstance(keys_values, dict):
        return jsformat(keys_values)
    if isinstance(keys_values, (list, tuple, set)):
        if all([is_ntuple(x, 2) for x in keys_values]):
            return jsformat(dict(keys_values))
        elif all([isinstance(x, str) for x in keys_values]):
            out = ['{']
            for k in keys_values:
                out.append('{1}{0}: {0}'.format(k, (indent + 4) * ' '))


def _gather(template, context, i, closing_mark):
    last = ''
    char = ''
    out = []
    closing_mark = '`' + closing_mark
    while last + char != closing_mark:
        i += 1
        out.append(last)
        last = char
        char = template[i]
    out = ''.join(out)
    out = (context[out])
    return (out, i)


def parse_template(template, context):
    lastlast = None
    last = None
    i = 0
    out = []
    while i < len(template):
        char = template[i]
        if char == '`':
            if lastlast != '\\' and last != '\\':
                (segment, i) = _templates[last](template, context, i+1)
            lastlast = None
            out += segment
            last = None
        else:
            i += 1
            out.append(char)
            lastlast = last
            last = char
    return ''.join(out)
