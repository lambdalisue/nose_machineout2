#from distutils import setup
from setuptools import setup

setup(
    name="nose_machineout",
    version="0.2",
    description="""\
Changes output of the nose testing tool into format easily parsable by machine.""",
    author="Max Ischenko",
    author_email="ischenko@gmail.com",
    url="http://maxischenko.in.ua/blog/entries/109/nose-vim-integration",
    download_url="http://cheeseshop.python.org/pypi/nose_machineout/0.1",
    install_requires = [
        "nose>=0.9",
    ],
    scripts = [],
    license="BSD",
    zip_safe=False,
    py_modules=['machineout', 'test_machineout'],
    entry_points = {
        'nose.plugins': ['machineout = machineout:NoseMachineReadableOutput'],
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

