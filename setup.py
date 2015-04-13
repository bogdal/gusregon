from setuptools import setup, find_packages

setup(
    name='django-gusregon',
    version='0.0.1',
    description='GUS REGON Internet Database Client',
    long_description=open('README.rst').read(),
    author='Adam Bogdal',
    author_email='adam@bogdal.pl',
    url='https://github.com/bogdal/django-gusregon',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'],
    install_requires=[
        'requests',
    ],
)
