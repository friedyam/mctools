#!/usr/bin/env python

import platform
from codecs import open
from os import (path, getenv)

from setuptools import setup
from version import VERSION

version = '.'.join([str(v) for v in VERSION])

THIS_DIR = path.dirname(path.realpath(__file__))

with open(path.join(THIS_DIR, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

license = 'GPL 3.0'

install_requires = [
    'click',
    'requests'
]

setup(
    name='mctools',
    version=version,
    description="Media Center Tools",
    long_description=long_description,
    author="Kris Wagner",
    author_email="kris1250@gmail.com",
    license=license,
    use_2to3=False,
    install_requires=install_requires,
    namespace_packages=[
        'mctools'
    ],
    packages=[
        'mctools',
        'mctools.mctools',
        'mctools.utils'
    ],
    package_dir={
        'mctools': '.',
        'mctools.mctools': './mctools',
        'mctools.utils': './utils'
    },
    package_data={
        'mctools.mctools': [
            'commands/*'
        ]
    },
    entry_points={
        'console_scripts': [
            'mctools = mctools.mctools.cli:cli'
        ]
    }
)
