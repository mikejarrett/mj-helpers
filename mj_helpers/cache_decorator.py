# -*- coding: utf-8 -*-
from functools import wraps
import inspect

try:
    from django.core.cache import cache

    def django_cache(cache_time=600, custom_prefix=None):

        """ Caches the data for ``cache_time`` seconds. """

        __cache_lock = threading.Lock()

        def decorator(func):

            @wraps(func)
            def inner(*args, **kwargs):
                # Little simplification to make same calls having same cache_key
                # by removing Nones and default values.
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

                # Redis key can not contain non ascii chars (cache_key is always
                # str, becouse of using repr)
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
except ImportError:
    print 'hello'
    pass
