import ops

def sic(func):
    func._hackkit_slightly__sic = True
    return func

def prettier(name, bases, dictionary, type=type):
    dict = {}
    for key, value in dictionary.iteritems():
        if key in ops.all:
            if hasattr(value, '_hackkit_slightly__sic'):
                del value._hackkit_slightly__sic
            else:
                key = '__' + key + '__'
        dict[key] = value
    return type(name, bases, dict)
