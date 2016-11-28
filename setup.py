# -*- coding: utf-8 -*-
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]
    test_args = []

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='gusregon',
    version='1.0.0',
    description='GUS REGON Internet Database Client',
    long_description=open('README.rst').read(),
    author='Adam Bogdał',
    author_email='adam@bogdal.pl',
    url='https://github.com/bogdal/gusregon',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'],
    install_requires=[
        'beautifulsoup4>=4.5.1',
        'lxml>=3.6.4',
        'suds-jurko>=0.6'
    ],
    cmdclass={
        'test': PyTest
    },
    tests_require=[
        'pytest>=2.8.1',
        'pytest-cov',
        'vcrpy>=1.7.3'
    ]
)
