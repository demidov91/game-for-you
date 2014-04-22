### -*- coding: utf-8 -*- ####################################################
#
# Copyright (c) 2009 Key UA. All Rights Reserved.
#
##############################################################################
"""
Configuration file used by setuptools. It creates 'egg', install all dependencies.

$Id$
"""

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

#Dependencies - python eggs
install_requires = [
	'pillow',
    'psycopg2',
    'django-allauth',
    'south==0.8.4',
]


#Execute function to handle setuptools functionality
setup(name="our_game",
      version="0.0.1",
      description="Web-tool for command games organization.",
      author="Demidov D. A.",
      packages=find_packages('src'),
      package_dir={'': 'src'},
      install_requires=install_requires,
      )
