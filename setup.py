#!/usr/bin/env python
"""
Changes output of the nose testing tool into format easily parsable
by a machine.

Originally written by Max Ischenko.
"""

from setuptools import setup

setup(
    name="nose_machineout",
    version="0.2",
    description=__doc__,
    author="Mike Crute",
    author_email="mcrute@gmail.com",
    url="http://bitbucket.org/mcrute/nose_machineout",
    install_requires = [
        "nose>=0.10",
    ],
    scripts = [],
    license="BSD",
    zip_safe=False,
    py_modules=['machineout', 'test_machineout'],
    entry_points = {
        'nose.plugins.0.10': ['machineout = machineout:NoseMachineReadableOutput'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    keywords='test unittest nose',
    test_suite = 'nose.collector')
