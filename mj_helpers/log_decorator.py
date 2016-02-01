# -*- coding: utf8 -*-
"""
Logging decorator that logs function name, args and kwargs.

Usage:
    from decorators import log_function_io

    @log_function_io()
    def foo(bar, spam=None, *args, **kwargs):
        return do_stuff()
"""
from collections import OrderedDict
from functools import wraps
import functools
import inspect
import itertools
import logging
import sys
import time


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class CustomAdapter(logging.LoggerAdapter):

    """Custom LoggerAdapter that adds metadata to the log message."""

    skip_processing_tags = ('[ARG]', '[RET]', '[FUN]')
    skip_msg_tag_tags = ('[POST]', '[GET]')

    def process(self, msg, kwargs):
        """Adds additional metadata to log message.

        Takes passed log message and adds additional metadata, like function
        name and [FUN], [MSG] tags.

        If `msg` already has tags specified in `skip_processing_tags`, it
        returns original message.
        If `msg` has tag from `skip_msg_tag_tags`, it only adds [FUN] tag and
        skips adding [MSG] tag.

        :param str msg: Log string to process
        :param dict kwargs: Keyword arguments for log message
        :return: Processed message and original keyword arguments
        :rtype: tuple
        """
        def get_func_name():
            stack = inspect.stack()
            for index, frame in enumerate(stack):
                if frame[3] == 'process':
                    return stack[index + 2][3]

        if any(tag in msg for tag in self.skip_processing_tags):
            return msg, kwargs
        elif any(tag in msg for tag in self.skip_msg_tag_tags):
            msg = u'[FUN] {} {}'.format(get_func_name(), msg)
        else:
            msg = u'[FUN] {} [MSG] {}'.format(get_func_name(), msg)

        return msg, kwargs


def get_logger_adapter(name):
    """Returns Custom LoggerAdapter that adds '[MSG]' tag to log message.

    Function returns standard logger, if name of the module is
    'log_decorator', because we don't wont to get this tag in
    `log_function_io` decorator.

    :param str name: Name of the module, for which to get logger
    :return: Logger adapter for given module
    :rtype: CustomAdapter
    """
    logger = logging.getLogger(name)
    return CustomAdapter(logger, {})


def log_function_io(f):

    log = getattr(
        sys.modules[f.__module__],
        'log',
        get_logger_adapter(f.__module__)
    )

    @wraps(f)
    def wrapper(*args, **kwargs):
        args_name = list(
            OrderedDict.fromkeys(inspect.getargspec(f)[0] + kwargs.keys())
        )
        args_dict = OrderedDict(
            list(itertools.izip(args_name, args)) +
            list(kwargs.iteritems())
        )

        # We don't care about `self` or `cls`
        args_dict.pop('self', None)
        args_dict.pop('cls', None)

        # Build a log_message with argument name and value
        log_args_message = ', '.join(
            '{}: %r'.format(arg_name.encode('utf-8'))
            for arg_name in args_dict.keys()
        )

        if log_args_message:
            log_args_message = '[FUN] {} [ARG] {} '.format(
                f.func_name,
                log_args_message
            )
        else:
            log_args_message = '[FUN] {} [ARG] No arguments'.format(
                f.func_name
            )
        log.debug(log_args_message, *args_dict.values())

        return_value = f(*args, **kwargs)

        log_return_value_message = '[FUN] {} [RET] {}'.format(
            f.func_name,
            repr(return_value).decode('utf-8')
        )

        log.debug(log_return_value_message)

        return return_value

    return wrapper
