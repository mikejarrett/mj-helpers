MJ Helpers
==========

A collection of helper functions and decorators that I occasionally use to get
my life in order.

Installation
------------

    pip install mj_helpers

profileit
---------

A decorator to profile function calls.

Usage::

    from mj_helpers.decorators import profileit

    @profileit
    def foo():
        return do_stuff()


In a Python shell::

    >>> from .foo import foo
    >>> foo()
    >>> from pstats import Stats
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

log_function_io
---------------

Logging decorator that logs function name, args and kwargs.

In Python:: 

    from mj_helpers.log_decorator import log_function_io
    
    @log_function_io
    def foo(bar, spam=None, *args, **kwargs):
        return do_stuff()


    class Thing(object):
        pass


    class Bar(object):

        @staticmethod
        @log_function_io
        def static_method(spam, eggs='eggs'):
            return True

        @classmethod
        @log_function_io
        def class_method(cls, foo='foo', bar=None):
            return False


        @log_function_io
        def function(self, thing):
            return Thing()

        
Console::

    >>> foo('a', *['first star', 'second star'], **{'something': 'boo'})
    2016-02-02 05:04:50,963 - __main__ - DEBUG - [FUN] foo [ARG] bar: 'a', spam: 'first star', something: 'boo' *('second star',)
    2016-02-02 05:04:50,963 - __main__ - DEBUG - [FUN] foo [RET] None

    >>> Bar.static_method('spam')
    2016-02-02 05:09:30,426 - __main__ - DEBUG - [FUN] static_method [ARG] spam: 'spam'
    2016-02-02 05:09:30,426 - __main__ - DEBUG - [FUN] static_method [RET] True

    >>> Bar.class_method(bar='spam')
    2016-02-02 05:11:39,753 - __main__ - DEBUG - [FUN] class_method [ARG] bar: 'spam'
    2016-02-02 05:11:39,753 - __main__ - DEBUG - [FUN] class_method [RET] False

    >>> Bar().function(thing='spam')
    2016-02-02 05:13:01,679 - __main__ - DEBUG - [FUN] function [ARG] thing: 'spam'
    2016-02-02 05:13:01,679 - __main__ - DEBUG - [FUN] function [RET] <__main__.Thing object at 0x7f33d8627f90>

cache_it
--------

Caching decorator to assist in caching function calls / returns.

In Python::

    from mj_helpers.decorators import cache_it

    @cache_it()
    def foo(bar, spam=None, *args, **kwargs):
        return do_stuff()

    # If using memoize instead of django's cache you can see the cache by:
    >>> cache_it._cache
    {
        <function foo at 0x7f4419daa848>: {
            "(('a', 'first star', 'second star'), (('something', 'boo'),))":
            (None, 1454391947.614329)
        }
    }
