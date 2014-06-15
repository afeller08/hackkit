
arith = [
    'add', 'sub',
    'mul', 'div', 'truediv', 'mod', 'floordiv',
    'pow', 'rshift', 'lshift', 
    'and', 'or', 'xor',
]

arithmetic =  [ m + op for op in arith for m in ['', 'i', 'r']]

object = [
    'new', 'init', 'del',
    'getattr', 'setattr', 'getattribute', 'delattr',
    'dict', 'slots',
    'class', 'metaclass',
    'isinstance', 'issubclass',
    'hash',
    'doc',
    'nonzero',
]

function = [
    'call',
]

comparison = [
    'le', 'ge',
    'eq', 'neq',
    'leq', 'geq',
]

string = ['str', 'repr', 'unicode']

obsolete = ['cmp', 'rcmp',]

descriptor = [
    'get', 'set', 'delete',
]

iterator = [
    'getitem', 'setitem', 'delitem',
    'getslice', 'delslice', 'setslice',
    'iter', 'contains', 
    'len',
    'reversed', 
]

coersion = [
    'coerce',
]

context = ['enter', 'exit']

sign = ['neg', 'pos', 'invert', 'abs']

all = (arithmetic + object + string + comparison + descriptor +
       function + iterator + coersion + context)
