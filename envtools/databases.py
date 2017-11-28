# encoding=UTF-8
from __future__ import unicode_literals

import logging
from collections import namedtuple
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

logger = logging.getLogger(__name__)


class DatabaseConfig(namedtuple("DatabaseConfig", "schema name host user password port options")):

    @classmethod
    def parse_url(cls, url):
        logger.debug(url)
        parsed = urlparse.urlparse(url)
        logger.debug(parsed)
        schema = cls.get_schema(scheme=parsed.scheme)
        factory = getattr(cls, 'create_{}'.format(schema), cls.create_default)
        return factory(parsed)

    @classmethod
    def create_default(cls, parsed_url):
        schema = cls.get_schema(scheme=parsed_url.scheme)
        options_factory = getattr(cls, 'create_{}_options'.format(schema), cls.create_options)
        options = options_factory(parsed_url.query)
        return cls(
            schema=schema,
            name=urlparse.unquote(parsed_url.path[1:]),
            host=parsed_url.hostname and urlparse.unquote(parsed_url.hostname),
            user=parsed_url.username and urlparse.unquote(parsed_url.username),
            password=parsed_url.password and urlparse.unquote(parsed_url.password),
            port=parsed_url.port,
            options=options
        )

    @classmethod
    def create_sqlite3(cls, parsed_url):
        if parsed_url.path:
            name = urlparse.unquote(parsed_url.path)
        else:
            name = ":memory:"
        return cls(
            schema='sqlite',
            name=name,
            host=None,
            user=None,
            password=None,
            port=None,
            options={}
        )

    @classmethod
    def get_schema(cls, scheme):
        schemas = {
            'sqlite': 'sqlite3',
            'postgres': 'postgresql',
            'mysqlgis': 'mysql',
            'oraclegis': 'oracle'
        }
        return schemas.get(scheme, scheme)

    @classmethod
    def create_options(cls, query_string):
        options = {}
        if query_string:
            options = urlparse.parse_qs(query_string)
            options.update({
                key: value[0]
                for key, value in options.items()
                if len(value) == 1
            })
        return options

    @classmethod
    def create_mysql_options(cls, query_string):
        options = cls.create_options(query_string)
        if 'reconnect' in options:
            del options['reconnect']
        if 'ssl-ca' in options:
            ca = options['ssl-ca']
            del options['ssl-ca']
            options['ssl'] = {'ca': ca}
        return options

    @classmethod
    def create_postgresql_options(cls, query_string):
        options = cls.create_options(query_string)
        if 'currentSchema' in options:
            current_schema = options['currentSchema']
            del options['currentSchema']
            options['options'] = '-c search_path={}'.format(current_schema)
        return options

    @classmethod
    def create_postgis_options(cls, query_string):
        return cls.create_postgresql_options(query_string)

    @classmethod
    def create_redshift_options(cls, query_string):
        return cls.create_postgresql_options(query_string)
