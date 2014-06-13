import slightly


__metaclass__ = slightly.prettier

class Ordered(list):
    def init(self, old=[], partial_order=None):
        self.partial_order = partial_order

