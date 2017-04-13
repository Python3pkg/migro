#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import io
import re

from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='migro',
    version=find_version('migro', '__init__.py'),
    packages=['migro'],
    description='Another database migration tool',
    long_description=read('README.rst'),

    install_requires=[
        'psycopg2',
        'pyyaml',
        'click'
    ],

    entry_points={
        'console_scripts': [
            'migro = migro.cli:cli'
        ]
    },

    author='Aleksandr Koshkarev',
    author_email='aleksandr_koshkarev@hotmail.com',
    license='MIT',
    url='https://github.com/ALFminecraft/Migro',
    keywords=['postgres', 'migration'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Topic :: Database'
    ]
)

