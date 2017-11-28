# encoding=UTF-8
from __future__ import unicode_literals

from .environment import get_env

__all__ = ['configure_logging']


def configure_logging(config_dict):
    prefix = 'LOGGING_'
    configured_dict = config_dict.copy()
    for logger_name in configured_dict['loggers']:
        env_suffix = logger_name.replace('.', '_')
        env_name = '{prefix}LEVEL_{suffix}'.format(prefix=prefix, suffix=env_suffix)
        env_value = get_env(env_name, configured_dict['loggers'][logger_name]['level'])
        configured_dict['loggers'][logger_name]['level'] = env_value
    return configured_dict
