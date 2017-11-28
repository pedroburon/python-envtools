# encoding=UTF-8
from __future__ import unicode_literals

import unittest

from envtools.databases import DatabaseConfig


class TestParseDatabaseURL(unittest.TestCase):

    def test_postgres_parsing(self):
        url = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'  # noqa
        expected = DatabaseConfig(
            schema='postgresql',
            name='d8r82722r2kuvn',
            host='ec2-107-21-253-135.compute-1.amazonaws.com',
            user='uf07k1i6d8ia0v',
            password='wegauwhgeuioweg',
            port=5431,
            options={}
        )

        config = DatabaseConfig.parse_url(url)

        self.assertEqual(expected, config)

    def test_postgres_unix_socket_parsing(self):
        url = 'postgres://%2Fvar%2Frun%2Fpostgresql/d8r82722r2kuvn'  # noqa
        expected = DatabaseConfig(
            schema='postgresql',
            name='d8r82722r2kuvn',
            host='/var/run/postgresql',
            user=None,
            password=None,
            port=None,
            options={}
        )

        config = DatabaseConfig.parse_url(url)

        self.assertEqual(expected, config)

    def test_ipv6_parsing(self):
        url = 'postgres://ieRaekei9wilaim7:wegauwhgeuioweg@[2001:db8:1234::1234:5678:90af]:5431/d8r82722r2kuvn'  # noqa
        expected = DatabaseConfig(
            schema='postgresql',
            name='d8r82722r2kuvn',
            host='2001:db8:1234::1234:5678:90af',
            user='ieRaekei9wilaim7',
            password='wegauwhgeuioweg',
            port=5431,
            options={}
        )

        config = DatabaseConfig.parse_url(url)

        self.assertEqual(expected, config)

    def test_postgres_search_path_parsing(self):
        url = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn?currentSchema=otherschema'  # noqa
        expected = DatabaseConfig(
            schema='postgresql',
            name='d8r82722r2kuvn',
            host='ec2-107-21-253-135.compute-1.amazonaws.com',
            user='uf07k1i6d8ia0v',
            password='wegauwhgeuioweg',
            port=5431,
            options={'options': '-c search_path=otherschema'}
        )

        config = DatabaseConfig.parse_url(url)

        self.assertEqual(expected, config)

    def test_postgres_parsing_with_special_characters(self):
        url = 'postgres://%23user:%23password@ec2-107-21-253-135.compute-1.amazonaws.com:5431/%23database'  # noqa
        expected = DatabaseConfig(
            schema='postgresql',
            name='#database',
            host='ec2-107-21-253-135.compute-1.amazonaws.com',
            user='#user',
            password='#password',
            port=5431,
            options={}
        )

        config = DatabaseConfig.parse_url(url)

        self.assertEqual(expected, config)

    def test_postgis_parsing(self):
        url = 'postgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'  # noqa
        expected = DatabaseConfig(
            schema='postgis',
            name='d8r82722r2kuvn',
            host='ec2-107-21-253-135.compute-1.amazonaws.com',
            user='uf07k1i6d8ia0v',
            password='wegauwhgeuioweg',
            port=5431,
            options={}
        )

        config = DatabaseConfig.parse_url(url)

        self.assertEqual(expected, config)

    def test_postgis_search_path_parsing(self):
        url = 'postgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn?currentSchema=otherschema'  # noqa
        expected = DatabaseConfig(
            schema='postgis',
            name='d8r82722r2kuvn',
            host='ec2-107-21-253-135.compute-1.amazonaws.com',
            user='uf07k1i6d8ia0v',
            password='wegauwhgeuioweg',
            port=5431,
            options={'options': '-c search_path=otherschema'}
        )

        config = DatabaseConfig.parse_url(url)

        self.assertEqual(expected, config)

    def test_mysql_gis_parsing(self):
        url = 'mysqlgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'  # noqa
        expected = DatabaseConfig(
            schema='mysql',
            name='d8r82722r2kuvn',
            host='ec2-107-21-253-135.compute-1.amazonaws.com',
            user='uf07k1i6d8ia0v',
            password='wegauwhgeuioweg',
            port=5431,
            options={}
        )
        config = DatabaseConfig.parse_url(url)

        self.assertEqual(expected, config)

    def test_mysql_connector_parsing(self):
        url = 'mysql-connector://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'  # noqa
        expected = DatabaseConfig(
            schema='mysql-connector',
            name='d8r82722r2kuvn',
            host='ec2-107-21-253-135.compute-1.amazonaws.com',
            user='uf07k1i6d8ia0v',
            password='wegauwhgeuioweg',
            port=5431,
            options={}
        )

        config = DatabaseConfig.parse_url(url)

        self.assertEqual(expected, config)

    def test_mysql_ssl_ca_parsing(self):
        url = 'mysql://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:3306/d8r82722r2kuvn?ssl-ca=rds-combined-ca-bundle.pem'  # noqa
        expected = DatabaseConfig(
            schema='mysql',
            name='d8r82722r2kuvn',
            host='ec2-107-21-253-135.compute-1.amazonaws.com',
            user='uf07k1i6d8ia0v',
            password='wegauwhgeuioweg',
            port=3306,
            options={'ssl': {'ca': 'rds-combined-ca-bundle.pem'}}
        )

        config = DatabaseConfig.parse_url(url)

        self.assertEqual(expected, config)

    def test_cleardb_parsing(self):
        url = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
        expected = DatabaseConfig(
            schema='mysql',
            name='heroku_97681db3eff7580',
            host='us-cdbr-east.cleardb.com',
            user='bea6eb025ca0d8',
            password='69772142',
            port=None,
            options={}
        )

        config = DatabaseConfig.parse_url(url)

        self.assertEqual(expected, config)

    def test_empty_sqlite_url(self):
        url = 'sqlite://'
        expected = DatabaseConfig(
            schema='sqlite',
            name=':memory:',
            host=None,
            user=None,
            password=None,
            port=None,
            options={}
        )

        config = DatabaseConfig.parse_url(url)

        self.assertEqual(expected, config)

    def test_memory_sqlite_url(self):
        url = 'sqlite://:memory:'
        expected = DatabaseConfig(
            schema='sqlite',
            name=':memory:',
            host=None,
            user=None,
            password=None,
            port=None,
            options={}
        )

        config = DatabaseConfig.parse_url(url)

        self.assertEqual(expected, config)

    def test_file_sqlite_url(self):
        url = 'sqlite:///path/to/database.sqlite'
        expected = DatabaseConfig(
            schema='sqlite',
            name='/path/to/database.sqlite',
            host=None,
            user=None,
            password=None,
            port=None,
            options={}
        )

        config = DatabaseConfig.parse_url(url)

        self.assertEqual(expected, config)

    def test_oracle_parsing(self):
        url = 'oracle://scott:tiger@oraclehost:1521/hr'
        expected = DatabaseConfig(
            schema='oracle',
            name='hr',
            host='oraclehost',
            user='scott',
            password='tiger',
            port=1521,
            options={}
        )

        config = DatabaseConfig.parse_url(url)

        self.assertEqual(expected, config)

    def test_oracle_gis_parsing(self):
        url = 'oraclegis://scott:tiger@oraclehost:1521/hr'
        expected = DatabaseConfig(
            schema='oracle',
            name='hr',
            host='oraclehost',
            user='scott',
            password='tiger',
            port=1521,
            options={}
        )

        config = DatabaseConfig.parse_url(url)

        self.assertEqual(expected, config)

    def test_oracle_dsn_parsing(self):
        url = (
            'oracle://scott:tiger@/'
            '(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)'
            '(HOST=oraclehost)(PORT=1521)))'
            '(CONNECT_DATA=(SID=hr)))'
        )
        expected = DatabaseConfig(
            schema='oracle',
            user='scott',
            password='tiger',
            host=None,
            port=None,
            name=(
                '(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)'
                '(HOST=oraclehost)(PORT=1521)))'
                '(CONNECT_DATA=(SID=hr)))'
            ),
            options={}
        )

        config = DatabaseConfig.parse_url(url)

        self.assertEqual(expected, config)

    def test_oracle_tns_parsing(self):
        url = 'oracle://scott:tiger@/tnsname'  # noqa
        expected = DatabaseConfig(
            schema='oracle',
            user='scott',
            password='tiger',
            name='tnsname',
            host=None,
            port=None,
            options={}
        )

        config = DatabaseConfig.parse_url(url)

        self.assertEqual(expected, config)

    def test_redshift_parsing(self):
        url = 'redshift://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5439/d8r82722r2kuvn?currentSchema=otherschema'  # noqa
        expected = DatabaseConfig(
            schema='redshift',
            name='d8r82722r2kuvn',
            host='ec2-107-21-253-135.compute-1.amazonaws.com',
            user='uf07k1i6d8ia0v',
            password='wegauwhgeuioweg',
            port=5439,
            options={'options': '-c search_path=otherschema'}
        )

        config = DatabaseConfig.parse_url(url)

        self.assertEqual(expected, config)

    def test_mssql_parsing(self):
        url = 'mssql://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com/d8r82722r2kuvn?driver=ODBC Driver 13 for SQL Server'  # noqa
        expected = DatabaseConfig(
            schema='mssql',
            name='d8r82722r2kuvn',
            host='ec2-107-21-253-135.compute-1.amazonaws.com',
            user='uf07k1i6d8ia0v',
            password='wegauwhgeuioweg',
            port=None,
            options={'driver': 'ODBC Driver 13 for SQL Server'}
        )

        config = DatabaseConfig.parse_url(url)

        self.assertEqual(expected, config)
