# Setup Python logging --------------------------------------------------------
import logging
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG,format=FORMAT)
LOG = logging.getLogger()

# Setup Path for files --------------------------------------------------------
import os
from time import time
from os.path import abspath
from collections import defaultdict
from tcp.common import __FILE_SEP
__PATH = abspath("files/") + "/"

def update_dir():
    # This function updates the files dictionary to show when the files were last changed.
    gen = os.walk(__PATH)
    _files = gen.next()[-1]
    del gen

    files = defaultdict(float)

    for filename in _files:
        tme = os.stat(__PATH + filename).st_atime
        if files[filename] != tme:
            files[filename] = tme

    return files

def update_file(filename):
    try:
        tme = os.stat(__PATH + filename).st_atime
    except OSError as e:
        LOG.error(e)
        return 0
    return tme

def create_file(filename):
    try:
        file_handle = open(__PATH + filename, "w")
        file_handle.write(" ")
        file_handle.close()
        file_handle = open(__PATH + filename, "r")
        return file_handle
    except IOError as e:
        LOG.error(e)

    return None


def get_file(filename, force = True):
    try:
        LOG.debug("Opening file %s"%(__PATH + filename))
        file_handle = open(__PATH + filename, "r")
    except IOError as e:
        LOG.error(e)
        file_handle = None
    if file_handle == None:
        if force:
            LOG.debug("Creating a new one.")
            file_handle = create_file(filename)
        else:
            return None
    m = file_handle.read()
    file_handle.close()

    return m

def change_file(filename, changes):
    try:
        file_handle = open(__PATH + filename, "w")
        file_handle.write(changes)
        file_handle.close()
    except IOError as e:
        LOG.error(e)
        return -1
    return 0

def get_dir():
    gen = os.walk(__PATH)
    _files = gen.next()[-1]
    del gen
    return __FILE_SEP.join(_files)
