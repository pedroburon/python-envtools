#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

import envtools


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    readme = f.read()


setup(
    name='python-envtools',
    version=envtools.__version__,
    description=envtools.__doc__,
    long_description=readme,
    packages=find_packages(exclude=('tests',)),
    setup_requires=['nose>=1.0', 'coverage'],
    install_requires=[],
    author=envtools.__author__,
    author_email='hi@pedroburon.info',
    url='https://github.com/pedroburon/python-envtools',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
