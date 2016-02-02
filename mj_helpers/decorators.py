# -*- coding: utf-8 -*-
try:
    from .cache_decorator import cache_it
except ImportError:
    pass

from .log_decorator import log_function_io

from .profileit import profileit
