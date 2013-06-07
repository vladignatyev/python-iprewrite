# coding: utf-8

__author__ = 'ya.na.pochte@gmail.com'

from setuptools import setup, find_packages

setup(name = "iprewrite",
    author="Vladimir Ignatev",
    author_email="ya.na.pochte@gmail.com",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    entry_points={
        'console_scripts':['iprewrite = iprewrite:main']
    },
    install_requires=["ipaddr==2.1.10",],
)
