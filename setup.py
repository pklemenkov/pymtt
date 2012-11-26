#!/usr/bin/env python
from distutils.core import setup

setup(name='PyMTT',
      version='1.0',
      description='Python Config Generator',
      author='Pavel Klemenkov',
      author_email='pklemenkov@gmail.com',
      url='https://github.com/pklemenkov/pymtt',
      requires=[
          'Jinja2 (>=2.3)'
      ],
      scripts=[
          'bin/pymtt'
      ]
      )