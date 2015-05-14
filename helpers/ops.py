def full(ops):
    return set(['__{0}__'.format(op) for op in ops])

arith = [
    'add', 'sub',
    'mul', 'div', 'truediv', 'mod', 'floordiv',
    'pow', 'rshift', 'lshift',
    'and', 'or', 'xor',
]

arithmetic = tuple([m + op for op in arith for m in ['', 'i', 'r']])

inplace_arith = dict(
    [('__{0}__'.format(op), '__i{0}__'.format(op)) for op in arith]
)

outplace_arith = dict(
    [('__i{0}__'.format(op), '__{0}__'.format(op)) for op in arith]
)

normal_arith = dict(
    [('__i{0}__'.format(op), '__{0}__'.format(op)) for op in arith] +
    [('__r{0}__'.format(op), '__{0}__'.format(op)) for op in arith]
)


left_arith = dict(
    [('__r{0}__'.format(op), '__{0}__'.format(op)) for op in arith]
)

right_arith = dict(
    [('__{0}__'.format(op), '__r{0}__'.format(op)) for op in arith]
)


object = (
    'new', 'init', 'del',
    'getattr', 'setattr', 'getattribute', 'delattr',
    'dict', 'slots',
    'class', 'metaclass',
    'instancecheck', 'subclasscheck',
    'hash',
    'doc',
    'nonzero',
)

function = (
    'call',
)

comparison = (
    'le', 'ge',
    'eq', 'neq',
    'leq', 'geq',
)

string = ('str', 'repr', 'unicode')

obsolete = ('cmp', 'rcmp')

descriptor = (
    'get', 'set', 'delete',
)

iterator = (
    'getitem', 'setitem', 'delitem',
    'getslice', 'delslice', 'setslice',
    'iter', 'contains',
    'len',
    'reversed',
)

coersion = (
    'coerce', 'trunc',
)

context = ('enter', 'exit')

sign = ('neg', 'pos', 'invert', 'abs')

all = (arithmetic + object + string + comparison + descriptor +
       function + iterator + coersion + context)


all_ops = tuple(['__{0}__'.format(op) for op in all])
