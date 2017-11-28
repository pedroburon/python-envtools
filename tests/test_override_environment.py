
import os
import unittest

from envtools import override_environment
from . import create_unique_env_name


class TestOverrideEnvironmentContextManager(unittest.TestCase):
    def test_override_nothing(self):
        os.environ['SOMETHING'] = existent = 'anything'
        with override_environment():
            self.assertEqual(os.getenv('SOMETHING'), existent)

    def test_override_var(self):
        os.environ['SOMETHING'] = existent = 'anything'
        expected = 'New Value'
        with override_environment(SOMETHING=expected):
            self.assertEqual(os.getenv('SOMETHING'), expected)
        self.assertEqual(os.getenv('SOMETHING'), existent)

    def test_override_vars(self):
        os.environ['FOO'] = existent_foo = 'baz'
        os.environ['BAR'] = existent_bar = 'anything'
        expected_foo = 'foo'
        expected_bar = 'bar'
        with override_environment(FOO=expected_foo, BAR=expected_bar):
            self.assertEqual(os.getenv('FOO'), expected_foo)
            self.assertEqual(os.getenv('BAR'), expected_bar)
        self.assertEqual(os.getenv('FOO'), existent_foo)
        self.assertEqual(os.getenv('BAR'), existent_bar)

    def test_stringify(self):
        os.environ['FOO'] = existent_foo = 'baz'
        os.environ['BAR'] = existent_bar = 'anything'
        expected_foo = 1
        expected_bar = False
        with override_environment(FOO=expected_foo, BAR=expected_bar):
            self.assertEqual(os.getenv('FOO'), str(expected_foo))
            self.assertEqual(os.getenv('BAR'), str(expected_bar))
        self.assertEqual(os.getenv('FOO'), existent_foo)
        self.assertEqual(os.getenv('BAR'), existent_bar)

    def test_delete(self):
        env = create_unique_env_name()
        os.environ[env] = 'foo'

        with override_environment(**{env: None}):
            self.assertNotIn(env, os.environ)
        self.assertEqual('foo', os.environ[env])

    def test_delete_non_existent(self):
        env = create_unique_env_name()

        with override_environment(**{env: None}):
            self.assertNotIn(env, os.environ)
        self.assertNotIn(env, os.environ)


class TestOverrideEnvironmentDecorator(unittest.TestCase):
    def test_override_nothing(self):
        os.environ['SOMETHING'] = existent = 'anything'

        @override_environment()
        def func():
            self.assertEqual(os.getenv('SOMETHING'), existent)
        func()

    def test_override_var(self):
        os.environ['SOMETHING'] = existent = 'anything'
        expected = 'New Value'

        @override_environment(SOMETHING=expected)
        def func():
            self.assertEqual(os.getenv('SOMETHING'), expected)
        func()
        self.assertEqual(os.getenv('SOMETHING'), existent)

    def test_override_vars(self):
        os.environ['FOO'] = existent_foo = 'baz'
        os.environ['BAR'] = existent_bar = 'anything'
        expected_foo = 'foo'
        expected_bar = 'bar'

        @override_environment(FOO=expected_foo, BAR=expected_bar)
        def func():
            self.assertEqual(os.getenv('FOO'), expected_foo)
            self.assertEqual(os.getenv('BAR'), expected_bar)
        func()
        self.assertEqual(os.getenv('FOO'), existent_foo)
        self.assertEqual(os.getenv('BAR'), existent_bar)

    def test_stringify(self):
        os.environ['FOO'] = existent_foo = 'baz'
        os.environ['BAR'] = existent_bar = 'anything'
        expected_foo = 1
        expected_bar = False

        @override_environment(FOO=expected_foo, BAR=expected_bar)
        def func():
            self.assertEqual(os.getenv('FOO'), str(expected_foo))
            self.assertEqual(os.getenv('BAR'), str(expected_bar))
        func()
        self.assertEqual(os.getenv('FOO'), existent_foo)
        self.assertEqual(os.getenv('BAR'), existent_bar)

    def test_delete(self):
        env = create_unique_env_name()
        os.environ[env] = 'foo'

        @override_environment(**{env: None})
        def func():
            self.assertNotIn(env, os.environ)
        func()
        self.assertEqual('foo', os.environ[env])

    def test_delete_non_existent(self):
        env = create_unique_env_name()

        @override_environment(**{env: None})
        def func():
            self.assertNotIn(env, os.environ)

        func()

        self.assertNotIn(env, os.environ)
