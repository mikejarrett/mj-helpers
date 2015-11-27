# MJ Helpers

A collection of helper functions and decorators that I occasionally use to get
my life in order.

## profileit

Usage:

    from profileit import profileit

    @profileit
    def foo():
        return do_stuff()

In a Python shell:

    >>> from .foo import foo
    >>> foo()
	>>> form pstats import Stats
	>>> stats = Stats('/tmp/foo.profile')
	>>> stats.sort_stats('cumulative').print_stats(50)

    Fri Nov 27 08:34:14 2015    /tmp/foo.profile
    2 function calls in 0.000 seconds

    Ordered by: cumulative time
    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
         1    0.000    0.000    0.000    0.000 <ipython-input-8-8f35865ca12d>:1(foo)
         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

## logit

TODO
