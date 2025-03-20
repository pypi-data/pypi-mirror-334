#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-module-docstring,exec-used
import setuptools

# DO NOT EDIT THIS NUMBER!
# It is changed automatically by python-semantic-release
__version__ = "0.1.0"

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name='symmetry_analysis',
    version=__version__,
    author='William Morrillo',
    author_email='williammorrillo@gmail.com',
    description='A programme for analysing molecular (pseudo)-point group symmetry',
    long_description=long_description,
    long_description_content_type='text/markdown',
    project_url={
        "Bug Tracker": "https://github.com/williammorrillo/symmetry_analysis/issues",
        "Documentation": "https://williammorrillo.gitlab.io/symmetry_analysis",
        "Source": "https://github.com/williammorrillo/symmetry_analysis",
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent'
        ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'vasp_suite',
        ],
    entry_points={
        'console_scripts': [
            'symmetry_analysis = src.cli'
            ]
        }
    )
    

