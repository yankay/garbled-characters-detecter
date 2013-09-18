#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'garbled_characters_detecter']

requires = ["chardet"]

setup(
    name='garbled_characters_detecter',
    version=1.0,
    description='Detect garbled characters, and find the reason.',
    long_description=open('README.md').read(),
    author='Kay Yan',
    author_email='yankaycom@gmail.com',
    url='https://github.com/yankay/garbled-characters-detecter',
    packages=packages,
    package_data={'': ['LICENSE', 'NOTICE'], 'garbled_characters_detecter': ['*.txt']},
    package_dir={'garbled_characters_detecter': 'garbled_characters_detecter'},
    include_package_data=True,
    install_requires=requires,
    license=open('LICENSE').read(),
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ),
)