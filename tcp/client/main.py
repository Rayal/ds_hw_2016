#!/usr/bin/python
#
# Implements File Service TCP client
#
# -----------------------------------------------------------------------------
'''
Message board client (TCP)
Created on Aug 23, 2016

@author: devel
'''
# Setup Python logging ------------------ -------------------------------------
import logging
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG,format=FORMAT)
LOG = logging.getLogger()
# Needed imports ------------------ -------------------------------------------
from tcp.client import protocol
from tcp.client.protocol import request_directory, request_file, edit_file,\
    request_update
import tcp.fileservice as fs
from tcp.common import __FILE_SEP
from time import localtime, asctime, sleep
from sys import stdin
# Not a real main method-------------------------------------------------------
def client_main(args):
    # Starting client
    server = (args.host,int(args.port))

    while True:
        sv_dr = request_directory(server)[0].split(__FILE_SEP)
        my_dr = fs.get_dir().split(__FILE_SEP)
        for fle in sv_dr:
            if not fle in my_dr:
                LOG.info("Getting new file %s from server"%fle)
                get_file(server, fle)
                my_dr.append(fle)

        for fle in my_dr:
            sv_tme = float(request_update(server, fle))
            my_tme = fs.update_file(fle)
            if my_tme < sv_tme:
                LOG.info("Updating file %s from server"%fle)
                get_file(server, fle)
            if my_tme > sv_tme:
                LOG.info("Updating file %s to server"%fle)
                push_file(server, fle)
        sleep(1)

    #fl = request_file(server, "random_name")

    #print ("Request file: ", fl)

    #ed = edit_file(server, "random_name", "changes made")

    #print ("Edit file: ", ed)

    #fl = request_file(server, "random_name")

    #print ("Request file:", fl)


    print 'Terminating ...'

def get_file(server, filename):
    file_data = request_file(server, filename)[0]
    fs.change_file(filename, file_data)

def push_file(server, filename):
    file_data = fs.get_file(filename, False)
    edit_file(server, filename, file_data)
