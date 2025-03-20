# setup_lifffile.py

"""Lifffile module setuptools script."""

import re

from setuptools import setup

setup(
    name='lifffile',
    version='2025.1.25',
    license='BSD',
    description='Lifffile is a placeholder for the liffile package.',
    author='Christoph Gohlke',
    author_email='cgohlke@cgohlke.com',
    url='https://www.cgohlke.com',
    project_urls={
        'Bug Tracker': 'https://github.com/cgohlke/liffile/issues',
        'Source Code': 'https://github.com/cgohlke/liffile',
        # 'Documentation': 'https://',
    },
    install_requires=['liffile'],
    platforms=['any'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
)
