# Setup Python logging --------------------------------------------------------
import logging
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG,format=FORMAT)
LOG = logging.getLogger()

# Setup Path for files --------------------------------------------------------
import os
from os.path import abspath
__PATH = abspath("files/") + "/"

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
    print(gen)
    res = ""
    for folder in gen:
        r = folder[0][len(__PATH):] + ";"
        for f in folder[1]:
            r += " "
            r += f
        r += ";"
        for f in folder[2]:
            r += " "
            r += f
        res += r + "|"
    return res
