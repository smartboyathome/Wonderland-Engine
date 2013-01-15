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