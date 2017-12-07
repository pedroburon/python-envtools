===============
python-envtools
===============

.. image:: https://travis-ci.org/pedroburon/python-envtools.svg?branch=master
   :target: https://travis-ci.org/pedroburon/python-envtools

.. image:: https://coveralls.io/repos/github/pedroburon/python-envtools/badge.svg?branch=master
   :target: https://coveralls.io/github/pedroburon/python-envtools?branch=master

Useful environment toolchain for python

********************
override_environment
********************

Context Processor that overrides environment vars.

::

    >>> @override_environment(DEBUG=False, FOO="Bar")
    >>> def foo():
    >>>     print(os.getenv("FOO"))
    >>>     return os.getenv("DEBUG")
    >>> foo()
    FOO
    "DEBUG"


::

    >>> with override_environment(DEBUG="False", FOO="Bar"):
    >>>     print(os.getenv("FOO"))
    >>>     os.getenv("DEBUG")
    FOO
    "DEBUG"


*****************
configure_logging
*****************

Wrap a `configDict` inside configure_logging, then logging level could be controlled by environment variables

::

    LOGGING = configure_logging({
        "loggers": {
            "module": {
                "handlers": ["console"],
                "level": "INFO",
            },
        }
    })

For this example, environment variable must be set as `LOGGING_LEVEL_module=DEBUG`.


*******
get_env
*******

Similar to `os.getenv()` but evaluates string content (default) into simple python types.

::

    >>> os.environ['FOO'] = "1"
    >>> os.getenv('FOO')
    "1"
    >>> get_env('FOO')
    1

    >>> os.environ['FOO'] = "bar"
    >>> get_env('FOO')
    "bar"

    >>> os.environ['FOO'] = "True"
    >>> os.getenv('FOO')
    "True"
    >>> get_env('FOO')
    True

    >>> os.environ['FOO'] = "[1,2,3]"
    >>> os.getenv('FOO')
    "[1,2,3]"
    >>> get_env('FOO')
    [1, 2, 3]


it works for list, tuples, dictionaries, numbers, booleans and strings. And is safe!

    
