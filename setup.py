# -*- coding: utf-8 -*-
import codecs
import os
import re

from setuptools import setup


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, *parts)).read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='pyinfo',
    description='python environment info as phpinfo does with php',
    packages=['pyinfo'],
    version=find_version('pyinfo', '_pyinfo.py'),
    author="Vincenzo Farruggia",
    author_email="mastropinguino@networky.net",
    url='https://github.com/mastropinguino/pyinfo',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Terminals',
        'Topic :: Utilities'
    ],
    keywords=['python info', 'pyinfo', 'environment information'])
