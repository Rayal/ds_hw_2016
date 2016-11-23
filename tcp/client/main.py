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
from tcp.client.protocol import \
request_directory, request_file, edit_file
from time import localtime, asctime
from sys import stdin
# Not a real main method-------------------------------------------------------
def client_main(args):
    '''Runs the Mboard client
    should be run by the main mehtod of CLI or GUI application
    @param args: ArgParse collected arguments
    '''
    # Starting client
    server = (args.host,int(args.port))

    dr = request_directory(server)

    print ("Request dir: ", dr)

    fl = request_file(server, "random_name")

    print ("Request file: ", fl)

    ed = edit_file(server, "random_name", "changes made")

    print ("Edit file: ", ed)

    fl = request_file(server, "random_name")

    print ("Request file:", fl)

    dr = request_directory(server)

    print ("Request dir", dr)

    print 'Terminating ...'
