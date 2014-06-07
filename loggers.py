'''Provide easy configuration of output.

Use as settings.  In your configuration file, modify the behavior by
setting public method to a private method.  Only use the public methods
in your actual code.
'''

def _print(*args):
    for x in args:
        print x,
    print

log = _print
warn = _print
