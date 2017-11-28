
import unittest

from envtools import override_environment, configure_logging


class TestConfigureLoggingLevel(unittest.TestCase):
    @override_environment(LOGGING_LEVEL_module='DEBUG')
    def test_change_level(self):
        result = configure_logging({
            'loggers': {
                'module': {
                    'handlers': ['console'],
                    'level': 'INFO',
                },
            },
        })

        self.assertEqual(
            {
                'loggers': {
                    'module': {
                        'handlers': ['console'],
                        'level': 'DEBUG',
                    },
                },
            },
            result
        )

    @override_environment(LOGGING_LEVEL_module='INFO')
    def test_maintain_level(self):
        result = configure_logging({
            'loggers': {
                'module': {
                    'handlers': ['console'],
                    'level': 'INFO',
                },
            },
        })

        self.assertEqual(
            {
                'loggers': {
                    'module': {
                        'handlers': ['console'],
                        'level': 'INFO',
                    },
                },
            },
            result
        )

    @override_environment(LOGGING_LEVEL_module_submodule_subsub='DEBUG')
    def test_dotpath_level(self):
        result = configure_logging({
            'loggers': {
                'module.submodule.subsub': {
                    'handlers': ['console'],
                    'level': 'INFO',
                },
            },
        })

        self.assertEqual(
            {
                'loggers': {
                    'module.submodule.subsub': {
                        'handlers': ['console'],
                        'level': 'DEBUG',
                    },
                },
            },
            result
        )

    @override_environment(LOGGING_LEVEL_module_submodule_subsub='DEBUG')
    def test_non_existent(self):
        result = configure_logging({
            'loggers': {
                'module': {
                    'handlers': ['console'],
                    'level': 'INFO',
                },
            },
        })

        self.assertEqual(
            {
                'loggers': {
                    'module': {
                        'handlers': ['console'],
                        'level': 'INFO',
                    },
                },
            },
            result
        )
