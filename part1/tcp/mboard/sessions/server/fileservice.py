# Setup Python logging --------------------------------------------------------
import logging
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG,format=FORMAT)
LOG = logging.getLogger()

# Setup Path for files --------------------------------------------------------
import os
from os.path import abspath
__PATH = abspath("files/")

def create_file(filename):
    try:
        file_handle = open(__PATH + filename, "w")
        return file_handle
    except IOError:
        LOG.error("Unable to create file.")

    return None


def get_file(filename, force = True):
    try:
        file_handle = open(__PATH + filename, "r")
    except IOError:
        LOG.debug("File not found, methinks")
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
        file_handle = open(__PATH + filename, "r+")
    except IOError:
        LOG.error("Tried to write to non-existent file")
    return 0

def get_dir():
    gen = os.walk(__PATH)
    res = ""
    for folder in gen:
        r = folder[0] + ";"
        for f in folder[1]:
            r += " "
            r += f
        r += ";"
        for f in folder[2]:
            r += " "
            r += f
        res += r + "\n"
    return res
