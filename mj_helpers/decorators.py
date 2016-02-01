# -*- coding: utf-8 -*-
try:
    from .cache_decorator import django_cache
except ImportError:
    print 'no django_cache'
    pass

from .log_decorator import log_function_io

from .profileit import profileit
