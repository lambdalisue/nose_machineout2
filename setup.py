# coding=utf-8
import sys
from setuptools import setup, find_packages

NAME = 'nose_machineout2'
VERSION = '0.5.1'


def read(filename):
    import os
    BASE_DIR = os.path.dirname(__file__)
    filename = os.path.join(BASE_DIR, filename)
    with open(filename, 'r') as fi:
        return fi.read()


def readlist(filename):
    rows = read(filename).split("\n")
    rows = [x.strip() for x in rows if x.strip()]
    return list(rows)

# if we are running on python 3, enable 2to3 and
# let it use the custom fixers from the custom_fixers
# package.
extra = {}
if sys.version_info >= (3, 0):
    extra.update(
        use_2to3=True,
    )

setup(
    name=NAME,
    version=VERSION,
    description=('Changes output of the nose testing tool into format easily'
                 'parsable by a machine.'),
    long_description = read('README.rst'),
    classifiers = (
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
    ),
    keywords = 'test unittest nose',
    author = 'Alisue',
    author_email = 'lambdalisue@hashnote.net',
    url = 'https://github.com/lambdalisue/%s' % NAME,
    download_url = 'https://github.com/lambdalisue/%s/tarball/master' % NAME,
    license = 'BSD',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data = True,
    package_data = {
        '': ['README.rst',
             'requirements.txt',
             'requirements-test.txt'],
    },
    zip_safe=True,
    install_requires=readlist('requirements.txt'),
    test_suite='nose.collector',
    tests_require=readlist('requirements-test.txt'),
    entry_points = {
        'nose.plugins.0.10': [
            'machineout = nose_machineout:NoseMachineReadableOutput'
        ],
    },
    **extra
)
