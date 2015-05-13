from helpers import loggers
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
    inherited_attributes_are_not_in_the_dict = True
    the_dict_passed_into_type_is_not_ordered = True

    def __init__(self, a):
        self.a = a

    def find(self):
        return self.a


class Second(First):
    value = "Metaclass functions don't get called by subclass."
    this_would_show_up_if_they_did = True


class Third(Second):
    __metaclass__ = metaclass
    if_you_asign_the_metaclass_function_to_a_subclass_it_will_run_again = True

    def __init__(self, a):
        self.a = a
        self.b = a + 6

    def find(self):
        return self.b


class Metaclass(type):
    def __new__(cls, name, bases, dict):
        for x in dict:
            if x.count('_') > 4:
                loggers.log(' '.join(x.split('_')))
        return super(Metaclass, cls).__new__(cls, name, bases, dict)


class Frist(object):
    __metaclass__ = Metaclass
    whereas_function_metaclassed_dont_get_rerun_when_inherited = True


class AlmostFrist(Frist):
    metaclasses_that_are_created_as_types_get_run_when_inherited = True


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
    loggers.log('super creates a strong reference.')
except:
    loggers.log('Otherwise, you would see this.')
