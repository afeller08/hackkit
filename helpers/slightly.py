import ops
import functools

def sic(func):
    func._hackkit_slightly__sic = True
    return func


def _prettier_dict(dictionary, bases):
    dict = {}
    inheritance = set()
    map(inheritance.union, [dir(x) for x in bases])
    for key, value in dictionary.iteritems():
        if key in ops.all:
            _key_ = '__{0}__'.format(key)
            if hasattr(value, '_hackkit_slightly__sic'):
                del value._hackkit_slightly__sic
            elif _key_ in inheritance or not key in inheritance:
                key = _key_
                value.__name__ = _key_
        dict[key] = value
    return dict


def prettier(name, bases, dictionary, type=type):
    dict = _prettier_dict(dictionary, bases)
    return type(name, bases, dict)


class Prettier(type):
    def __new__(cls, name, bases, dict):
        return prettier(name, bases, dict)


def inferred(name, bases, dict, type=type):
    if '__add__' in dict and not '__radd__' in dict:
        def __radd__(self, other):
            return self + other
        dict['__radd__'] = __radd__
    if '__mul__' in dict and not '__rmul__' in dict:
        def __rmul__(self, other):
            return self * other
        dict['__rmul__'] = __rmul__
    if '__and__' in dict and not '__rand__' in dict:
        def __rand__(self, other):
            return self & other
        dict['__rand__'] = __rmul__
    if '__or__' in dict and not '__ror__' in dict:
        def __ror__(self, other):
            return self | other
        dict['__ror__'] = __ror__
    if '__xor__' in dict and not '__rxor__' in dict:
        def __rxor__(self, other):
            return self ^ other
        dict['__rxor__'] = __rxor__
    if '__mul__' in dict and not '__neg__' in dict:
        def __neg__(self):
            return self * -1
        dict['__neg__'] = __neg__
    if '__add__' in dict and '__neg__' in dict and not '__sub__' in dict:
        def __sub__(self, other):
            try:
                return self + -other
            except:
                return -(-self + other)
        dict['__sub__'] = __sub__
    if '__add__' in dict and '__neg__' in dict and not '__rsub__' in dict:
        def __rsub__(self, other):
            return -self + other
        dict['__rsub__'] = __rsub__
    if '__pow__' in dict and not '__rdiv__' in dict:
        def __rdiv__(self, other):
            return other * self ** -1
        dict['__rdiv__'] = __rdiv__
    if '__rdiv__' in dict and not '__div__' in dict:
        def __div__(self, other):
            return 1 / (other/self)
        dict['__div__'] = __div__
    if '__div__' in dict and not '__truediv__' in dict:
        dict['__truediv__'] = dict['__div__']
    if '__rdiv__' in dict and not '__rtruediv__' in dict:
        dict['___rtruediv__'] = dict['_rdiv__']
    if '__truediv__' in dict and not '__div__' in dict:
        dict['__div__'] = dict['__truediv__']
    if '__rtruediv__' in dict and not '__rdiv__' in dict:
        dict['__rdiv__'] = dict['__rtruediv__']
    if '__floordiv__' in dict and '__sub__' in dict and not '__mod__' in dict:
        def __mod__(self, other):
            return self - ((self // other) * other)
        dict['__mod__'] = __mod__
    if '__setslice__' in dict and not '__setitem__' in dict:
        def __setitem__(self, i, v):
            self[i:i] = [v]
        dict['__setitem__'] = __setitem__
    if '__getslice__' in dict and not '__getitem__' in dict:
        def __getitem__(self, i):
            return self[i:i][0]
        dict['__getitem__'] = __getitem__
    if '__delslice__' in dict and not '__delitem__' in dict:
        def __delitem__(self, i):
            del self[i:i]
        dict['__delitem__'] = __delitem__
    if '__rshift__' in dict and not '__lshift__' in dict:
        def __lshift__(self, other):
            return self >> -other
        dict['__lshift__'] = __lshift__
    if '__lshift__' in dict and not '__rshift__' in dict:
        def __rshift__(self, other):
            return self << -other
        dict['__rshift__'] = __rshift__
    eqops = set(ops.full(ops.comparison))
    if '__eq__' in dict and len(set(dict.keys()).intersection(eqops)) > 1:
        return functools.total_ordering(type(name, bases, dict))
    else:
        return type(name, bases, dict)


class Inferred(type):
    def __new__(cls, name, bases, dict):
        return inferred(name, bases, dict)


def less_verbose(cls):
    '''Inherit doc string when overriding method unless has new doc string.'''
    sup = super(cls, cls)
    for attr in vars(cls):
        method = getattr(cls, attr)
        if hasattr(method, '__call__'):
            if not method.__doc__:
                if hasattr(sup, attr):
                    meth = getattr(sup, attr)
                    method.__doc__ = meth.__doc__
    return cls


def refined(name, bases, dictionary, type=type):
    dict = _prettier_dict(dictionary, bases)
    cls = prettier(name, bases, dictionary, inferred)
    return less_verbose(cls)


class Refined(type):
    def __new__(cls, name, bases, dict):
        return refined(name, bases, dict)
