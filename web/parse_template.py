import json


_templates = {}


def jsformat(thing):
    if hasattr(thing, '_hackkit__jsformat'):
        return thing._hackkit__jsformat()
    else:
        return json.dumps(thing)


def case(func, char):
    '''Extend parse_template by using @case('c').

    The decorated function creates a template for c`...`.
    c may be any character.
    '''
    _templates[char] = func
    return func


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
    return out, i


@case('(')
def _paren(template, context, i):
    (params, i) = _gather(template, context, i, ')')
    out = ['(']
    for x in params:
        if not isinstance(x, basestring):
            raise TypeError("_paren requires strings. TODO: better error")
        out.append(x)
    out.append(')')
    return ''.join(out), i


def is_ntuple(thing, n):
    if isinstance(thing, tuple) and len(thing) == n:
        return True
    return False


@case('{')
def _curly(template, context, i):
    keys_values, i = _gather(template, context, i, ')')
    if isinstance(keys_values, dict):
        return jsformat.dumps(keys_values), i
    if isinstance(keys_values, (list, tuple, set)):
        if all([is_ntuple(x, 2) for x in keys_values]):
            return jsformat(dict(keys_values)), i
        elif all([isinstance(x, str) for x in keys_values]):
            out = ['{']
            for k in keys_values:
                out.append('{0}: {0}'.format(k))
            out.append('}')
            return ', '.join(out), i


@case('[')
def _square(template, context, i):
    list, i = _gather(template, context, i, ']')
    return jsformat(list), i


@case("'")
def _quote(template, context, i):
    out, i = _gather(template, context, i, "'")
    return json.dumps(jsformat(out)), i


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
    return out, i


def parse_template(template, context):
    lastlast = None
    last = None
    i = 0
    out = []
    while i < len(template):
        char = template[i]
        if char == '`':
            if lastlast != '\\' and last != '\\':
                segment, i = _templates[last](template, context, i+1)
            lastlast = None
            out.append(segment)
            last = None
        else:
            i += 1
            out.append(char)
            lastlast = last
            last = char
    return ''.join(out)
