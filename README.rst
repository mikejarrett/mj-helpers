MJ Helpers
==========

A collection of helper functions and decorators that I occasionally use to get
my life in order.

Installation
------------

    pip install mj_helpers

profileit
--------

Usage::

    from profileit import profileit

    @profileit
    def foo():
        return do_stuff()


In a Python shell::

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
         
If installed via pip or python setup.py::

    mj_stats /tmp/foo.profile /tmp/bar.profile --sorting=cumulative --limit=50

log_it
------

In Python:: 

    from log_decorator import log_it
    
    class SomeClass(object):

    @staticmethod
    @log_it()
    def foo_static_method(bar, spam='spam', eggs=None, *args, **kwargs):
        pass

    @classmethod
    @log_it()
    def foo_class_method(cls, bar, spam='spam', eggs=None, *args, **kwargs):
        pass

    @log_it():
    def bar(self, foo, spam='spam', eggs=None, *args, **kwargs):
        pass
        
Console::

    >>> SomeClass.foo_static_method('bar')
    DEBUG:__main__:Entering foo(bar='bar', spam='spam', eggs=None)
    DEBUG:__main__:Exit foo -- Time in function: 0.00s

    >>> SomeClass.foo_class_method('bar')
    DEBUG:__main__:Entering foo(cls='cls', bar='bar', spam='spam', eggs=None)
    DEBUG:__main__:Exit foo -- Time in function: 0.00s

    >>> SomeClass().bar('foo', *['spam_arg', 'eggs_arg', 'another_arg'], a_kwarg='a_kwarg')
    DEBUG:__main__:Entering bar(self='self', foo='foo', spam='spam_arg', eggs='eggs_arg', *('another_arg',), **{'a_kwarg': 'a_kwarg'})
    DEBUG:__main__:Exit bar -- Time in function: 0.00s
