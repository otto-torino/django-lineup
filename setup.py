#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from lineup/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("lineup", "__init__.py")


if sys.argv[-1] == 'publish':
    try:
        import wheel
        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

REPO_URL = 'https://github.com/otto-torino/django-lineup'

setup(
    name='django-lineup',
    version=version,
    description="""Navigation system for django sites""",
    long_description=readme + '\n\n' + history,
    author='abidibo',
    author_email='abidibo@gmail.com',
    url=REPO_URL,
    packages=[
        'lineup',
        'lineup.templatetags',
        'lineup.management.commands',
    ],
    include_package_data=True,
    install_requires=[
        'django-mptt',
    ],
    license="MIT",
    zip_safe=False,
    keywords='django-lineup',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    project_urls={
        'Documentation': 'https://django-lineup.readthedocs.io/en/latest/',
        'Source': REPO_URL,
        'Tracker': REPO_URL + '/issues',
    },
)
