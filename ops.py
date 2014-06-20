from collections import defaultdict
arith = [
    'add', 'sub',
    'mul', 'div', 'truediv', 'mod', 'floordiv',
    'pow', 'rshift', 'lshift',
    'and', 'or', 'xor',
]

arithmetic = tuple([m + op for op in arith for m in ['', 'i', 'r']])

inplace_arith = defaultdict(
    [('__{0}__'.format(op), '__i{0}__'.format(op)) for op in arith], None
)

outplace_arith = defaultdict(
    [('__i{0}__'.format(op), '__{0}__'.format(op)) for op in arith], None
)

normal_arith = defaultdict(
    [('__i{0}__'.format(op), '__{0}__'.format(op)) for op in arith] +
    [('__r{0}__'.format(op), '__{0}__'.format(op)) for op in arith], None
)

left_arith = defaultdict(
    [('__r{0}__'.format(op), '__{0}__'.format(op)) for op in arith], None
)

right_arith = defaultdict(
    [('__{0}__'.format(op), '__r{0}__'.format(op)) for op in arith], None
)

object = (
    'new', 'init', 'del',
    'getattr', 'setattr', 'getattribute', 'delattr',
    'dict', 'slots',
    'class', 'metaclass',
    'isinstance', 'issubclass',
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
    'coerce',
)

context = ('enter', 'exit')

sign = ('neg', 'pos', 'invert', 'abs')

all = (arithmetic + object + string + comparison + descriptor +
       function + iterator + coersion + context)


all_ops = tuple(['__{0}__'.format(op) for op in all])
