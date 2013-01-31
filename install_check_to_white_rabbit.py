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

import WhiteRabbit, os, sys, argparse, shutil, py_compile

class CannotOpenFile(Exception):
    def __init__(self, directory):
        self.directory = directory
    def __repr__(self):
        return "Cannot write a file at '{}'.".format(self.directory)

if __name__ == '__main__':
    exit_code = 0
    parser = argparse.ArgumentParser(description="A tool to help install checks into White Rabbit.")
    parser.add_argument('python_file', nargs='*')
    args = parser.parse_args()
    check_dir = os.path.join(os.path.split(WhiteRabbit.__file__)[0], 'checks')
    if not os.path.exists(check_dir) or not os.access(check_dir, os.W_OK):
        raise CannotOpenFile(check_dir)
    for f in args.python_file:
        abspath = os.path.abspath(f)
        if not os.path.exists(abspath) or not os.access(abspath, os.R_OK):
            print "Could not read a file at '{}'.".format(abspath)
            exit_code = 1
            continue
        path, name = os.path.split(abspath)
        new_path = os.path.join(check_dir, name)
        shutil.copy(abspath, new_path)
        py_compile.compile(new_path)
    sys.exit(exit_code)