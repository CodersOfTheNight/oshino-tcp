#!/usr/bin/python
# -*- coding: UTF-8 -*-
from setuptools import setup

from oshino_tcp.version import get_version


setup(name="oshino_tcp",
      version=get_version(),
      description="TCP metrics receiver",
      author="Šarūnas Navickas",
      author_email="zaibacu@gmail.com",
      packages=["oshino_tcp"],
      install_requires=["oshino"],
      test_suite="pytest",
      tests_require=["pytest", "pytest-cov"],
      setup_requires=["pytest-runner"]
      )
