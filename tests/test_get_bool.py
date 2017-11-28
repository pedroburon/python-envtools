
import unittest
import uuid
from envtools import override_environment, get_bool


class TestGetBool(unittest.TestCase):
    def test_get_true_default_strings(self):
        true_strings = [
            "True",
            "true",
            "TRUE",
            "1"
        ]
        for true_string in true_strings:
            with override_environment(BOOL_VAR=true_string):
                self.assertTrue(get_bool('BOOL_VAR'))

    def test_get_true_strings_from_arg(self):
        true_strings = [
            "FOO",
            "BAR",
            "Baz"
        ]
        for true_string in true_strings:
            with override_environment(BOOL_VAR=true_string):
                self.assertTrue(get_bool('BOOL_VAR', true_strings=true_strings))

    def test_get_false(self):
        false_strings = [False, 'false', "None", 0]
        for false_string in false_strings:
            with override_environment(BOOL_VAR=false_string):
                self.assertFalse(get_bool('BOOL_VAR'))

    def test_get_false_on_non_existent(self):
        bool_var = str(uuid.uuid4()).replace('-', '_')
        self.assertFalse(get_bool(bool_var))

    def test_get_true_on_non_existent(self):
        bool_var = str(uuid.uuid4()).replace('-', '_')
        self.assertTrue(get_bool(bool_var, True))
