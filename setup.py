import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open('requirements.txt') as fp:
    requires = [r.strip() for r in fp.readlines()]

setup(
    name='rawa',
    version='0.0.1',
    classifiers=[],
    author='Hs Silesia',
    author_email='marpiechula@gmail.com',
    url='https://github.com/hackerspace-silesia/rawa',
    packages=find_packages(),
    install_requires=requires,
    tests_require=requires,
)