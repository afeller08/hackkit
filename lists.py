import slightly


__metaclass__ = slightly.prettier


class Ordered(list):
    '''
    Not meant to subclass other derivatives of list.
    '''
    def init(self, list_=[], **kwargs):
        if '_sorted' in kwargs:
            list.__init__(self, sorted(list_))
        else:
            list.__init__(self, list_)

    def add(self, other):
        if not isinstance(other, Ordered):
            other = sorted(other)
        J = self
        K = other
        lj = len(self)
        lk = len(other)
        k = j = 0
        combined = []
        Jj = J[j]
        Kk = K[k]
        while k < lk and j < lj:
            if Kk < Jj:
                combined.append(Kk)
                k += 1
                Kk = K[k]
            else:
                combined.append(Jj)
                j += 1
                Jj = J[j]
        while k < lk:
            combined.append(K[k])
            k += 1
        while j < Jj:
            combined.append(J[j])
            j += 1
        return Ordered(combined, True)

    def intersects(self, other, **kwargs):
        intersection = None
        if '_intersection' in kwargs:
            intersection == []
        if not isinstance(other, Ordered):
            other = sorted(other)
        J = self
        K = other
        lj = len(self)
        lk = len(other)
        k = j = 0
        combined = []
        Jj = J[j]
        Kk = K[k]
        while k < lk and j < lj:
            if Kk < Jj:
                combined.append(Kk)
                k += 1
                Kk = K[k]
            else:
                combined.append(Jj)
                j += 1
                Jj = J[j]
        while k < lk:
            combined.append(K[k])
            k += 1
        while j < Jj:
            combined.append(J[j])
            j += 1
        return Ordered(combined, _sorted=True)

    setslice = NotImplemented
    setitem = NotImplemented

    def iadd(self, other):
        list.__setslice__(self, 0, len(self), self + other)
        return self

    def findindex(self, value):
        '''Return where value belongs even if value not in list.'''
        if not self:
            return 0
        step = len(self) // 2

    def contains(self, value):
        index = indindex(self, value)
        if self[index] == value:
            return True
        return False

    def index(self, value):
        if not self:
            raise ValueError('{0} not in list'.format(value))
        index = self.findindex(value)
        if self[index] != value:
            raise ValueError('{0} not in list'.format(value))
        return index

    def append(self, value):
        list.insert(self, self.findindex(value))
