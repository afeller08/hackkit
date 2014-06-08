

def deindex(iterable):
    '''Return a dict mapping the values to the keys of the iterable.'''
    result = {}
    if isinstance(iterable, dict):
        iterable = iterable.iteritems()
    for i, value in enumerate(iterable):
        result[value] = i
    return result 
