from python.collections import defaultdict as DefaultDict, OrderedDict

from superior import subclass
import bases


class Const(bases.Const):
    pass


RememberAll = (DefaultDict, OrderedDict)  # Silence pyflakes.


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
    def __call__(self, key, value=Const(None)):
        if value == Const(None):
            return self[key]
        else:
            self[key] = value
            return self


@subclass
class ModeDict(dict):
    def __init__(self, sup, *args, **kwargs):
        self.modes = []
        self.popmodes = []
        self.names = []
        return sup(*args, **kwargs)

    def push(self, **named_arg):
        name = named_arg.keys()
        if len(name) != 1:
            raise TypeError('takes exactly 1')  # TODO: dict type error
        name = name[0]
        mode = named_arg[name]
        self.names.append(name)
        popmode = {}
        self.popmodes.append(popmode)
        self.modes.append(mode)
        for (key, val) in mode.iteritems():
            k = Const(None)
            old = self.get(key, k)
            if old is not k:
                popmode[key] = old
            self[key] = val
