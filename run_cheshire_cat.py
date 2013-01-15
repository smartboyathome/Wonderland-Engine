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

import sys, argparse
from CheshireCat import create_app, run_app

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--config-dir", help="The directory in which the config is located")
    parser.add_argument("-c", "--config-file", help="The filename of the config file (without the directory name)")
    parser.add_argument("-s", "--configspec-file", help="The filename of the configspec file (without the directory name)")
    args = parser.parse_args()
    kwargs = {}
    if args.config_dir is not None:
        kwargs['_config_dir'] = args.config_dir
    if args.config_file is not None:
        kwargs['_config_filename'] = args.config_file
    if args.configspec_file is not None:
        kwargs['_configspec_filename'] = args.configspec_file
    create_app(**kwargs)
    run_app()
