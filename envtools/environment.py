# encoding=UTF-8
from __future__ import unicode_literals

import os
import functools
import ast
import logging

__all__ = ['override_environment', 'get_bool', 'get_env']

logger = logging.getLogger(__name__)


DEFAULT_TRUE_STRINGS = (
    "True",
    "true",
    "TRUE",
)


def get_env(name, default=None):
    try:
        value = os.environ[name]
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        logger.debug("cannot eval environment")
        return value
    except KeyError:
        if default is not None:
            return default
        raise KeyError("No environment variable named {}".format(name))


def get_bool(name, default=False, true_strings=DEFAULT_TRUE_STRINGS):
    value = get_env(name, default)
    if isinstance(value, bool):
        return value
    elif isinstance(value, str):
        return value in true_strings
    return bool(value)


class override_environment(object):
    """
    Context manager and decorator for override environment variables.

    >>> @override_environment(DEBUG=False, FOO='Bar')
    ... def foo():
    ...     print(os.getenv('DEBUG'))
    ...     return os.getenv('FOO')
    >>> foo()
    False
    'Bar'
    >>> with override_environment(DEBUG='False', FOO='Bar'):
    ...     print(os.getenv('FOO'))
    ...     os.getenv('DEBUG')
    Bar
    'False'
    """
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __enter__(self):
        self.existent = {}
        for key, value in self.kwargs.items():
            if key in os.environ:
                self.existent[key] = os.environ[key]

            if value is not None:
                os.environ[key] = str(value)
            elif key in os.environ:
                del os.environ[key]

    def __exit__(self, exc_type, exc_value, traceback):
        for key in self.kwargs:
            if key in self.existent:
                os.environ[key] = self.existent[key]
            elif key in os.environ:
                del os.environ[key]

    def __call__(self, func):
        @functools.wraps(func)
        def decorator(*args, **kwds):
            with self:
                return func(*args, **kwds)
        return decorator
