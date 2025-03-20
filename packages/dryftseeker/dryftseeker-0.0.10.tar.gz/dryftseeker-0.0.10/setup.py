#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages, Extension

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [ ]

test_requirements = [ ]

setup(
    author="Meinolf Sellmann",
    author_email='info@insideopt.com',
    python_requires='>=3.8.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.8',
        'Operating System :: POSIX :: Linux'
    ],
    description="InsideOpt Seeker Linux 38 - 311 Distribution",
    install_requires=requirements,
    long_description=readme, 
    keywords='insideopt, seeker, optimization',
    name='dryftseeker',
    test_suite='tests',
    version='0.0.10',
    packages=find_packages(include=['dryftseeker', 'dryftseeker.*', '*.so']),
    package_data={'dryftseeker': ['*.so', 'dryftseeker.py', 'bin/*', 'scripts/*']},
    zip_safe=False,
)
