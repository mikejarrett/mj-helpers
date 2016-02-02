# -*- coding: utf-8 -*-
"""
Caching decorator to assist in caching function calls / returns.

Usage:
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
"""
from functools import wraps
import inspect
import logging
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


try:
    from django.core.cache import cache

    def cache_it(cache_time=600, custom_prefix=None):

        """ Caches the data for ``cache_time`` seconds. """

        __cache_lock = threading.Lock()

        def decorator(func):

            @wraps(func)
            def inner(*args, **kwargs):
                # Little simplification to make same calls having same
                # cache_key by removing Nones and default values.
                # Also .defaults can be None, in such case we need to change
                # it into empty list for zip() to work
                func_args = inspect.getargspec(func)
                default_args = dict(
                    zip(
                        reversed(func_args.args or []),
                        reversed(func_args.defaults or [])
                    )
                )
                cache_key_kwargs = {
                    key: val for key, val in kwargs.iteritems()
                    if not (val is None or val == default_args.get(key))
                }
                cache_key = repr(func) + repr(args) + repr(cache_key_kwargs)

                # Redis key can not contain non ascii chars (cache_key is
                # always str, because of using repr)
                cache_key = cache_key.decode('utf-8')
                if custom_prefix:
                    cache_key = custom_prefix + cache_key

                with __cache_lock:
                    if cache_key not in cache:
                        result = func(*args, **kwargs)
                        cache.set(cache_key, result, cache_time)
                        return result

                    return cache.get(cache_key)

            return inner

        return decorator

except ImportError as err:
    logger.exception("Couldn't import Django, defaulting to memoize.")
    import time

    class cache_it(object):

        """ Memoize With Timeout.

        Borrowed with love from:
        http://code.activestate.com/recipes/325905-memoize-decorator-with-timeout/
        """
        _caches = {}
        _timeouts = {}

        def __init__(self, cache_time=600, custom_prefix=None):
            self.timeout = cache_time
            self.custom_prefix = custom_prefix

        def collect(self):
            """ Clear cache of results which have timed out. """
            for func in self._caches:
                cache = {}
                for key in self._caches[func]:
                    time_ = time.time() - self._caches[func][key][1]
                    if time_ < self._timeouts[func]:
                        cache[key] = self._caches[func][key]

                self._caches[func] = cache

        def __call__(self, function):
            self.cache = self._caches[function] = {}
            self._timeouts[function] = self.timeout

            def func(*args, **kwargs):
                keys = sorted(kwargs.items())
                key = repr((args, tuple(keys)))
                if self.custom_prefix:
                    key = repr(self.custom_prefix) + key

                try:
                    value = self.cache[key]
                    if (time.time() - value[1]) > self.timeout:
                        raise KeyError

                except KeyError:
                    value = self.cache[key] = function(*args, **kwargs), time.time()

                return value[0]
            func.func_name = function.__name__

            return func
