# encoding=UTF-8
from __future__ import unicode_literals

import logging

from .. import get_env
from ..databases import DatabaseConfig

logger = logging.getLogger(__name__)

DEFAULT_ENV = 'DATABASE_URL'


class DjangoDatabaseConfig(DatabaseConfig):
    SCHEMAS = {
        'postgres': 'django.db.backends.postgresql_psycopg2',
        'postgresql': 'django.db.backends.postgresql_psycopg2',
        'pgsql': 'django.db.backends.postgresql_psycopg2',
        'postgis': 'django.contrib.gis.db.backends.postgis',
        'mysql': 'django.db.backends.mysql',
        'mysql2': 'django.db.backends.mysql',
        'mysqlgis': 'django.contrib.gis.db.backends.mysql',
        'mysql-connector': 'mysql.connector.django',
        'mssql': 'sql_server.pyodbc',
        'spatialite': 'django.contrib.gis.db.backends.spatialite',
        'sqlite': 'django.db.backends.sqlite3',
        'oracle': 'django.db.backends.oracle',
        'oraclegis': 'django.contrib.gis.db.backends.oracle',
        'redshift': 'django_redshift_backend',
    }
    conn_max_age = 0

    def as_dict(self):
        config = {
            'ENGINE': self.engine,
            'NAME': self.name,
            'HOST': self.host,
            'USER': self.user,
            'PASSWORD': self.password,
            'PORT': self.port,
            'CONN_MAX_AGE': self.conn_max_age
        }
        if self.options:
            config['OPTIONS'] = self.options
        return config

    @property
    def engine(self):
        if not hasattr(self, '_engine') or self._engine is None:
            self._engine = self.get_django_engine(self.schema)
        return self._engine

    @engine.setter
    def engine(self, engine):
        self._engine = engine

    @classmethod
    def get_django_engine(cls, schema):
        try:
            return cls.SCHEMAS[schema]
        except KeyError:
            logger.info("Missing engine for schema %s", schema)
            raise KeyError("Cannot configure django database with schema '{}'".format(schema))


def configure_database(env=DEFAULT_ENV, default=None, engine=None, conn_max_age=0):
    try:
        url = get_env(env, default)
    except KeyError:
        logger.info("No environment variable (%s) for django configuration", env)
        return {}
    else:
        config = DjangoDatabaseConfig.parse_url(url)
        config.engine = engine
        config.conn_max_age = conn_max_age
        return config.as_dict()
