import loggers
import gc
import weakref

def metaclass(name, bases, dict):
    for x in dict:
        if x.count('_') > 4:
            loggers.log(' '.join(x.split('_')) + '.')
    return type(name, bases, dict)

class Base(object):
    thing = 3
    otherthing = 4
    whatever = 5


class First(Base):
    __metaclass__ = metaclass
    Inherited_attributes_are_not_in_the_dict = True
    def __init__(self, a):
        self.a = a
    def find(self):
        return self.a


class Second(First):
    value = "Subclasses don't excercise inherrited metaclasses."
    This_would_show_up_if_they_did = True

class Third(Second):
    __metaclass__ = metaclass
    You_must_redeclare_them_to_use_them_in_a_subclass = True
    def __init__(self, a):
        self.a = a
        self.b = a + 6
    def find(self):
        return self.b
        

first = First(2)
w = weakref.proxy(first)
w.find()
del first
gc.collect()
try:
    w.find()
    loggers.log("This won't get logged because...")
except:
    loggers.log('weakrefs get garbage collected as expected.')



third = Third(3)
s = super(Third, third)
del third
gc.collect()

s.find()


try:
    s.find()
    loggers.log('Super creates a strong reference.')
except:
    loggers.log('Otherwise, you would see this.')
