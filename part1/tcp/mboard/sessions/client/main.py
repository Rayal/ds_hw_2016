#!/usr/bin/python
#
# Implements message board TCP client
#
# Switching to TCP protocol allows us to avoid programming of our own sessions
# for big-block delivery. TCP connections are in fact a data delivery sessions.
# Therefore in this implementation we just removed everything
# related to the sessions protocol, that we implemented for UDP.
# When sending a request the client first connects to server,
# then request/response sequence starts.
#
# --------------
#
# Simple command-line application
# Currently no interactive mode implemented, application does the request
# and dies. User has to provide the IP address of the server at least.
# Default behavior is to fetch all the messages from the Board and show them
# to the user. Refer to --help to get the details about the options.
#
# Current implementation considers all user input is by default in UTF-8, no
# additional encoding.
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
from tcp.mboard.sessions.client import protocol
from tcp.mboard.sessions.client.protocol import \
request_directory, request_file, edit_file
from time import localtime, asctime
from sys import stdin
# Constants -------------------------------------------------------------------
___NAME = 'MBoard Client'
___VER = '0.1.0.0'
___DESC = 'Simple Message Board Client (TCP version)'
___BUILT = '2016-09-13'
___VENDOR = 'Copyright (c) 2016 DSLab'
# Private methods -------------------------------------------------------------
def __info():
    return '%s version %s (%s) %s' % (___NAME, ___VER, ___BUILT, ___VENDOR)
# Not a real main method-------------------------------------------------------
def mboard_client_main(args):
    '''Runs the Mboard client
    should be run by the main mehtod of CLI or GUI application
    @param args: ArgParse collected arguments
    '''
    # Starting client
    LOG.info('%s version %s started ...' % (___NAME, ___VER))
    LOG.info('Using %s version %s' % ( protocol.___NAME, protocol.___VER))
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
