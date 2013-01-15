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
import sys

def get_root_dir():
    if hasattr(sys, 'real_prefix'):
        return sys.prefix
    else:
        return os.path.split(sys.prefix)[0]

def get_first_file_that_exists(dir_list, filename):
    for d in dir_list:
        f = os.path.join(d, filename)
        if os.path.exists(f):
            return f
    return None

def load_plugins(path):
    dir_list = os.listdir(path)
    mods = {}
    for fname in dir_list:
        try:
            if os.path.isdir(os.path.join(path, fname)) and os.path.exists(os.path.join(path, fname, '__init__.py')):
                f, filename, descr = imp.find_module(fname, [path])
                mods[fname] = imp.load_module(fname, f, filename, descr)
            elif os.path.isfile(os.path.join(path, fname)):
                name, ext = os.path.splitext(fname)
                if ext == '.py' and not name == '__init__':
                    f, filename, descr = imp.find_module(name, [path])
                    mods[name] = imp.load_module(name, f, filename, descr)
        except Exception:
            continue
    return mods

class FileNotFound(Exception):
    def __init__(self, file_type, searched_dirs, filename):
        self.file_type = file_type
        self.searched_dirs = searched_dirs
        self.filename = filename
    def __str__(self):
        retval = "Cannot find any {file_type} files named '{filename}' in the following directories:\n".format(file_type=self.file_type, filename=self.filename)
        for d in self.searched_dirs:
            retval = retval + d + "\n"
        retval = retval + "Please make sure the file exists in one of these directories before rerunning this command."
        return retval