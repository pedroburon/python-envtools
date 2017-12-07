#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
from os import path

import envtools

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()

setup(
    name='python-envtools',
    version=envtools.__version__,
    description='Python environment toolchain',
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
