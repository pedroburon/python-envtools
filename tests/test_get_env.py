# encoding=UTF-8
from __future__ import unicode_literals

import unittest

from envtools import get_env, override_environment
from . import create_unique_env_name


class TestGetEnvTypes(unittest.TestCase):
    def assert_get_env_value(self, value, expected):
        var_name = create_unique_env_name()
        with override_environment(**{var_name: value}):
            self.assertEqual(expected, get_env(var_name))

    def test_get_string(self):
        self.assert_get_env_value(value='asdf', expected='asdf')

    def test_get_number_string(self):
        self.assert_get_env_value(value='"1234"', expected='1234')

    def test_get_integer(self):
        self.assert_get_env_value(value='1234', expected=1234)

    def test_get_float(self):
        self.assert_get_env_value(value='12.34', expected=12.34)

    def test_get_true(self):
        self.assert_get_env_value(value='True', expected=True)

    def test_get_false(self):
        self.assert_get_env_value(value='False', expected=False)

    def test_get_list(self):
        self.assert_get_env_value(value='[1,2,"3"]', expected=[1, 2, "3"])

    def test_get_empty_tuple(self):
        self.assert_get_env_value(value='()', expected=())

    def test_get_tuple(self):
        self.assert_get_env_value(value='(1, 2)', expected=(1, 2))

    def test_get_dict(self):
        self.assert_get_env_value(value='{1:"2","b":("1",2)}', expected={1: "2", "b": ("1", 2)})

    def test_get_none(self):
        self.assert_get_env_value(value='None', expected=None)

    def test_get_invalid_syntax(self):
        self.assert_get_env_value(value='mysql://bea6eb025ca0d8', expected='mysql://bea6eb025ca0d8')


class TestGetEnv(unittest.TestCase):
    def test_get_default(self):
        name = create_unique_env_name()
        expected = "foo"

        self.assertEqual(expected, get_env(name, expected))

    def test_get_value(self):
        name = create_unique_env_name()
        expected = "foo"
        default = "bar"

        with override_environment(**{name: expected}):
            self.assertEqual(expected, get_env(name, default))

    def test_get_nothing(self):
        name = create_unique_env_name()

        self.assertRaisesRegexp(KeyError, "No environment variable named [\w_]+", get_env, name)
