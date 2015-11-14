"""
author: Rahul Mohandas
"""
from setuptools import setup

setup(
    name="warez-tools",
    version="0.1",
    packages=find_packages(exclude=["tests"]),
    author="Rahul Mohandas",
    author_email="rahul@rahulmohandas.com",
    description="Tools to handle Warez Standards",
    license="MIT",
    test_suite="tests"
)
