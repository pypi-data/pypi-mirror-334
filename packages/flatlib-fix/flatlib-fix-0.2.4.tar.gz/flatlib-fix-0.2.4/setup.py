"""
    This file is fix&update of flatlib - (C) FlatAngle
    Author: Jiaquan Dong (dongjiaquan89@gmail.com)

"""

from setuptools import setup
from setuptools import find_packages

setup(
    # Project
    name='flatlib-fix',
    version='0.2.4',

    # Sources
    packages=find_packages(),
    package_data={
        'flatlib': [
            'resources/README.md',
            'resources/swefiles/*'
        ],
    },

    # Dependencies
    install_requires=['pyswisseph>=2.10.03.2'],

    # Metadata
    description='Python library for Traditional Astrology',
    url='https://github.com/flatangle/flatlib',
    keywords=['Astrology', 'Traditional Astrology'],
    license='MIT',

    # Authoring
    author='João Ventura',
    author_email='flatangleweb@gmail.com',

    # Classifiers
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
