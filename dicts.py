from python.collections import defaultdict as DefaultDict, OrderedDict

from superior import subclass

@subclass
class RememberAll(dict):
    '''Create dict that rememembers past value.'''
    _hackkit_interface = [(RememberAll, dict)]
    def __init__(self, sup, dict={}, _RememberAll__mindepth=0, *args, **kws):
        self._RememberAll__mindepth = _RememberAll__mindepth
        sup(dict, **kws)

    def __setitem__(superior, key, value):
        try:
            stored = superior[key]
            stored.append(value)
        except KeyError:
            superior[key] = [value]

    def __getitem__(sup, key):
        return sup(key)[0]

    def pop(self, superior, key):
        stored = superior[key]
        if len(stored) > self._RememberAll_mindepth:
            if len(stored) == 1:
                val = stored[0]
                return val


class CallableDict(dict):
    def __call__(self, key):
        return self[value]


