# -*- coding: utf8 -*-
"""
A decorator to profile function calls.

Usage:
    from profileit import profileit

    @profileit
    def foo():
        return do_stuff()

In a Python shell:
    >>> form pstats import Stats
    >>> stats = Stats('/tmp/foo.profile')
    >>> stats.sort_stats('cumulative').print_stats(50)

"""
try:
    import cProfile as profile
except ImportError:
    import profile

def profileit(func):

    def wrapper(*args, **kwargs):
        datafn = '/tmp/{0}.profile'.format(func.__name__)
        prof = profile.Profile()
        retval = prof.runcall(func, *args, **kwargs)
        prof.dump_stats(datafn)

        return retval

    return wrapper
