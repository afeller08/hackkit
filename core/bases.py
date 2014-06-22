'''
Standard usage

class Const(HackKit.bases.Const):
   pass

Gives you a quick and easy way to produce constants that are shared throughout the file that created them.

Const('a') == Const('a')
Const('a') is Const('a')

Const('a') != HackKit.Bases.Const('a')


For Object:
You do the same thing, except more frequently

In each __init__.py in the project, you do
class Object(ParentDir.Object):
    pass

Then in each file, you do
class Object(MyDir.Object):
    pass

Doing so makes making comprehensive changes throughout the project much,
much easier later on. (E.g. you want to do an audit of creation
parameters, or log each time a value changes. You simply update
the appropriate base in one place and all of the changes propogate.)

'''

class Object(object):
    ''' Objects can be casted to subclasses and superclasses for free. 
        Siblings, cousins, etc. require an interemediate call to an
        ancestor. (Because all descendants of Object are distant cousins.)

        To pass in a subclass or superclass as the sole argument during
        creation, you only need provide a meaningless keyword argument
        (e.g. use_super=False).
    '''

    def __new__(cls, *args, **kargs):

        if len(args) == 1 and not kargs and \
            (isinstance(args[0], cls) or issubclass(cls,args[0].__class__)):

                n = super(Object, cls).__new__(cls)
                d = args[0].__dict__
                for x in d:
                    n.__dict__[x] = d[x]
                return n

        else:
            return super(Object, cls).__new__(cls, *args, **kargs)

    def __init__(self, *args, **kargs):
        '''__init__ can always call super'''
        pass

class _Object(Object):
    ''' Objs maintain an audit of their creation parameters. '''
    def __new__(cls, *args, **kargs):
        n = super(Obj, cls).__new__(cls, *args, **kargs)
        n.args = args
        n.kargs = kargs
        return n


class Const(object):
    initiated = {}
    def __new__(cls, val):
        if not val in cls.initiated:
            cls.initiated[val] = super(Constant, cls).__new__(cls) 
        return cls.initiated[val]

