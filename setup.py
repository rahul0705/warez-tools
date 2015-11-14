"""
author: Rahul Mohandas
"""
import setuptools

setuptools.setup(
    name="warez-tools",
    version="0.1",
    packages=setuptools.find_packages(exclude=["tests"]),
    author="Rahul Mohandas",
    author_email="rahul@rahulmohandas.com",
    description="Tools to handle Warez Standards",
    license="MIT",
    test_suite="tests"
)
