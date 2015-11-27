# -*- coding: utf8 -*-
"""
Logging decorator that logs function name, args and kwargs.

Usage:
    from log_decorator import log_it

    @log_it()
    def foo(bar, spam=None, *args, **kwargs):
        return do_stuff()
"""
import functools
import logging
import time


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class log_it(object):

    """ Logging decorator that allows you to log with a specific logger. """

    ENTRY_MESSAGE = 'Entering {0}'
    EXIT_MESSAGE = 'Exit {0} -- Time in function: {1:.2f}s'

    def __init__(self, logger=None):
        self.logger = logger

    def __call__(self, func):
        """
        Returns a wrapper that wraps func.

        The wrapper will log the entry and exit points of the function
        with logging.DEBUG level.
        """
        # Set logger if it was not set earlier
        if not self.logger:
            logging.basicConfig()
            self.logger = logging.getLogger(func.__module__)

        @functools.wraps(func)
        def wrapper(*func_args, **func_kwargs):
            message = self.do_the_things(func, func_args, func_kwargs)

            self.logger.debug(self.ENTRY_MESSAGE.format(message))

            entry_time = time.time()
            f_result = func(*func_args, **func_kwargs)
            exit_time = time.time()

            time_diff = exit_time - entry_time

            exit_message_args = (func.__name__, time_diff)
            self.logger.debug(self.EXIT_MESSAGE.format(*exit_message_args))
            return f_result

        return wrapper

    def do_the_things(self, func, func_args, func_kwargs):
        arg_names = func.__code__.co_varnames[:func.__code__.co_argcount]

        defaults = func.func_defaults or ()
        my_kwargs = func_kwargs.copy()

        params = zip(arg_names, func_args)
        params = self._handle_cls_and_self_params(params)
        params, remaining_kwargs = self._map_args_from_key_word_args(
            arg_names,
            my_kwargs,
            params
        )
        params = self._handle_default_arguments(
            params,
            arg_names,
            defaults
        )

        extra_star_params = self._get_extra_star_params(
            func_args,
            arg_names,
            remaining_kwargs
        )

        return self._get_log_message(func, params, extra_star_params)

    def _handle_cls_and_self_params(self, params):
        if params and params[0][0] == 'self':
            params[0] = ('self', 'self')
        if params and params[0][0] == 'cls':
            params[0] = ('cls', 'cls')

        return params

    def _map_args_from_key_word_args(self, arg_names, my_kwargs, params):
        for arg_name in arg_names:
            if arg_name in my_kwargs:
                params.append((arg_name, my_kwargs.pop(arg_name)))

        return params, my_kwargs

    def _handle_default_arguments(self, params, arg_names, defaults):
        if len(params) <= len(arg_names):
            params += zip(arg_names[len(params):], defaults)

        return params

    def _get_extra_star_params(self, func_args, params, my_kwargs):
        extra_args = func_args[len(params):]
        if extra_args:
            extra_args = ((', *', extra_args),)

        if my_kwargs:
            extra_args += ((', **', my_kwargs),)

        return extra_args

    @staticmethod
    def _get_log_message(func, params, extra_star_params):
        return '{0}({1}{2})'.format(
            func.__name__,
            ', '.join('%s=%r' % param for param in params),
            ''.join('%s%r' % param for param in extra_star_params)
        )
