#!/usr/bin/env python2

"""
    Copyright (c) 2012 Alexander Abbott

    This file is part of the Cheshire Cyber Defense Scoring Engine (henceforth
    referred to as Cheshire).

    Cheshire is free software: you can redistribute it and/or modify it under
    the terms of the GNU Affero General Public License as published by the
    Free Software Foundation, either version 3 of the License, or (at your
    option) any later version.

    Cheshire is distributed in the hope that it will be useful, but WITHOUT ANY
    WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
    FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
    more details.

    You should have received a copy of the GNU Affero General Public License
    along with Cheshire.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
from WonderlandUtils import get_root_dir

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='wonderland-engine',
    version='0.9',
    packages=['WhiteRabbit', 'WhiteRabbit.checks', 'Doorknob', 'CheshireCat',
              'CheshireCat.blueprints', 'CheshireCat.blueprints.checks',
              'CheshireCat.blueprints.teams'],
    py_modules=['WonderlandUtils'],
    scripts=['run_cheshire_cat.py', 'run_white_rabbit.py'],

    install_requires=[
        'Flask',
        'Jinja2',
        'Werkzeug',
        'redis',
        'configobj',
        'pymongo',
        'py-bcrypt',
        'Flask-Login',
        'parcon',
        'argparse'
    ],

    data_files=[
        (os.path.join(get_root_dir(), 'etc', 'wonderland-engine'), ['configspec.cfg', 'settings.cfg'])
    ],

    test_suite='nose.collector',
    tests_require='nose',
    url='http://smartboyathome.github.com/Wonderland-Engine/',
    license='AGPL',
    author='smartboyathome',
    author_email='smartboyathome@gmail.com',
    description='The Wonderland Cyber Defense Scoring Engine is a scoring engine for use in cyber defense competitions and practices. See the docs for more details.'
)