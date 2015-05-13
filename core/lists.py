import hackkit.helpers.slightly


class Ordered(list):
    '''
    Not meant to subclass other derivatives of list.
    '''
    def __init__(self, list_=[], **kwargs):
        if '_sorted' in kwargs:
            list.__init__(self, list_)
        else:
            list.__init__(self, sorted(list_))

    def __add__(self, other):
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
        while True:
            if Kk < Jj:
                combined.append(Kk)
                k += 1
                if k == lk:
                    break
                Kk = K[k]
            else:
                combined.append(Jj)
                j += 1
                if j == lj:
                    break
                Jj = J[j]
        while k < lk:
            combined.append(K[k])
            k += 1
        while j < lj:
            combined.append(J[j])
            j += 1
        return Ordered(combined, _sorted=True)

    def __iadd__(self, other):
        list.__init__(self, self + other)
        return self

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
        Jj = J[j]
        Kk = K[k]
        while k < lk and j < lj:
            if Kk < Jj:
                k += 1
                Kk = K[k]
            elif Kk == Jj:
                if intersection is None:
                    return True
                intersection.append(Kk)
                k += 1
                j += 1
                Kk = K[k]
                Jj = J[j]
            else:
                combined.append(Jj)
                j += 1
                Jj = J[j]
        if intersection is None:
            return False
        return Ordered(intersection, _sorted=True)

    setslice = NotImplemented
    setitem = NotImplemented

    def __and__(self, other):
        intersects(self, other, _intersection=True)

    def findindex(self, value):
        '''Return where value belongs even if value not in list.'''
        if not self:
            return 0
        length = len(self)
        step = length // 2
        position = step
        val = self[position]
        while step > 8:
            step //= 2
            if self[position] < value:
                position += step
            elif val == value:
                return position
            else:
                position -= step
            val = self[position]
        if val > value:
            position -= step
        elif value > self[-1]:
            return length
        val = self[position]
        while val < value:
            position += 1
            val = self[position]
        return position

    def __contains__(self, value):
        if len(self) < 16:
            return list.__contains__(self, value)
        index = findindex(self, value)
        if self[index] == value:
            return True
        return False

    def index(self, value):
        if not self:
            raise ValueError('{0} not in list'.format(value))
        if len(self) < 16:
            return list.index(self, value)
        i = self.findindex(value)
        if i == len(self) or self[i] != value:
            raise ValueError('{0} not in list'.format(value))
        return i

    def append(self, value):
        list.insert(self, self.findindex(value))
