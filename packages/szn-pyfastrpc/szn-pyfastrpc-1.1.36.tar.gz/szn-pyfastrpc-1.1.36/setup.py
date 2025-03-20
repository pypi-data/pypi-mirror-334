#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='szn-pyfastrpc',
    version='1.1.36',
    description='A FastRPC protocol implementation in Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Roman Skvara',
    author_email='skvara.roman@gmail.com',
    url='https://github.com/opicevopice/szn-pyfastrpc',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    install_requires=[
        'requests-html>=0.10.0'
    ],
    entry_points={
        'console_scripts': [
            # This entry point will call the open_readme() function defined in open_readme.py,
            'open-readme=szn_pyfastrpc.open_readme:open_readme'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
