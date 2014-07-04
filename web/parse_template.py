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
    elif isinstance(object, (set, list)):
        list = [jsformat(obj) for obj in object]
        list[0] = '[' + list[0]
        list[-1] += ']'
        return ', '.join(list)
    elif isinstance(object, dict):
        dict = [(jsformat(a), jsformat(b)) for (a, b) in object.iteritems()]
        dict = ['{0}: {1}'.format(a, b) for (a, b) in dict]
        return ', '.join(dict)


@case('`')
def _backtick(template, context, i):
    char = None
    out = []
    while char != '`':
        char = template[i]
        out.append(char)
        i += 1
    out = jsformat(context[out])
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
