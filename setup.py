#!/usr/bin/env python
from setuptools import setup

setup(name='pymtt',
      version='1.0',
      description='Python Config Generator',
      author='Pavel Klemenkov',
      author_email='pklemenkov@gmail.com',
      url='https://github.com/pklemenkov/pymtt',
      install_requires=[
          'Jinja2 >=2.3'
      ],
      scripts=[
          'bin/pymtt'
      ]
      )
