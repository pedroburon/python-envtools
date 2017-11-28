# encoding=UTF-8
from __future__ import unicode_literals

import unittest

from envtools import override_environment
from envtools.django import configure_database


class TestConfigureDatabase(unittest.TestCase):

    def assert_config(self, config, **params):
        self.assertEqual(params, config)

    def test_noconfig_database_url(self):
        with override_environment(DATABASE_URL=None):
            config = configure_database()
            self.assertEqual({}, config)

    def test_database_url(self):
        url = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'  # noqa

        with override_environment(DATABASE_URL=url):
            config = configure_database()

        self.assert_config(
            config,
            ENGINE='django.db.backends.postgresql_psycopg2',
            NAME='d8r82722r2kuvn',
            HOST='ec2-107-21-253-135.compute-1.amazonaws.com',
            USER='uf07k1i6d8ia0v',
            PASSWORD='wegauwhgeuioweg',
            PORT=5431,
            CONN_MAX_AGE=0
        )

    def test_config_engine_setting(self):
        engine = 'django_mysqlpool.backends.mysqlpool'
        url = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'  # noqa

        with override_environment(DATABASE_URL=url):
            config = configure_database(engine=engine)

        self.assertEqual(engine, config['ENGINE'])

    def test_config_conn_max_age_setting(self):
        conn_max_age = 600
        url = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'  # noqa

        with override_environment(DATABASE_URL=url):
            config = configure_database(conn_max_age=conn_max_age)

        self.assertEqual(conn_max_age, config['CONN_MAX_AGE'])

    def test_database_url_with_options(self):
        # Test full options
        url = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn?sslrootcert=rds-combined-ca-bundle.pem&sslmode=verify-full'  # noqa

        with override_environment(DATABASE_URL=url):
            config = configure_database()

        self.assert_config(
            config,
            ENGINE='django.db.backends.postgresql_psycopg2',
            NAME='d8r82722r2kuvn',
            HOST='ec2-107-21-253-135.compute-1.amazonaws.com',
            USER='uf07k1i6d8ia0v',
            PASSWORD='wegauwhgeuioweg',
            PORT=5431,
            OPTIONS={
                'sslrootcert': 'rds-combined-ca-bundle.pem',
                'sslmode': 'verify-full'
            },
            CONN_MAX_AGE=0
        )

    def test_database_url_without_options(self):
        # Test empty options
        url = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn?'  # noqa

        with override_environment(DATABASE_URL=url):
            config = configure_database()

        self.assertNotIn('OPTIONS', config)

    def test_mysql_database_url_with_sslca_options(self):
        url = 'mysql://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:3306/d8r82722r2kuvn?ssl-ca=rds-combined-ca-bundle.pem'  # noqa

        with override_environment(DATABASE_URL=url):
            config = configure_database()

        self.assert_config(
            config,
            ENGINE='django.db.backends.mysql',
            NAME='d8r82722r2kuvn',
            HOST='ec2-107-21-253-135.compute-1.amazonaws.com',
            USER='uf07k1i6d8ia0v',
            PASSWORD='wegauwhgeuioweg',
            PORT=3306,
            OPTIONS={
                'ssl': {
                    'ca': 'rds-combined-ca-bundle.pem'
                }
            },
            CONN_MAX_AGE=0
        )

    def test_mysql_database_url_without_sslca_options(self):
        # Test empty options
        url = 'mysql://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:3306/d8r82722r2kuvn?'  # noqa

        with override_environment(DATABASE_URL=url):
            config = configure_database()

        self.assertNotIn('OPTIONS', config)

    def test_config_unkown_schema(self):
        url = 'unknown://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:3306/d8r82722r2kuvn?'  # noqa

        with override_environment(DATABASE_URL=url):
            self.assertRaisesRegexp(
                KeyError, "Cannot configure django database with schema '\w*'", configure_database)
