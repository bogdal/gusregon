# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

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
)
