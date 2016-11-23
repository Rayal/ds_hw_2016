#!/usr/bin/python
#
# Implements remote file system TCP server
# -----------------------------------------------------------------------------
from tcp.mboard.sessions.server.protocol import __disconnect_client
# Setup Python logging ------------------ -------------------------------------
import logging
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG,format=FORMAT)
LOG = logging.getLogger()
# Imports ---------------------------------------------------------------------
from tcp.mboard.sessions.server import protocol
from tcp.mboard.sessions.common import tcp_receive, tcp_send, \
    MBoardProtocolError
from socket import socket, AF_INET, SOCK_STREAM
from socket import error as soc_error
from sys import exit
# How many clients may there be awaiting to get connection if the server is
# currently busy processing the other request
__DEFAULT_SERVER_TCP_CLIENTS_QUEUE = 10

def mboard_server_main(args):
    '''Runs the File Service server
    @param args: ArgParse collected arguments
    '''
    # Declaring TCP socket
    __server_socket = socket(AF_INET,SOCK_STREAM)
    LOG.debug('Server socket created, descriptor %d' % __server_socket.fileno())
    # Bind TCP Socket
    try:
        __server_socket.bind((args.listenaddr,int(args.listenport)))
    except soc_error as e:
        LOG.error('Can\'t start MBoard server, error : %s' % str(e) )
        exit(1)
    LOG.debug('Server socket bound on %s:%d' % __server_socket.getsockname())
    # Put TCP socket into listening state
    __server_socket.listen(__DEFAULT_SERVER_TCP_CLIENTS_QUEUE)
    LOG.info('Accepting requests on TCP %s:%d' % __server_socket.getsockname())

    # Declare client socket, set to None
    client_socket = None

    # Serve forever
    while 1:
        try:
            LOG.debug('Awaiting new client connections ...')
            # Accept client's connection store the client socket into
            # client_socket and client address into source
            client_socket,source = __server_socket.accept()
            LOG.debug('New client connected from %s:%d' % source)
            m = ''
            try:
                m = tcp_receive(client_socket)
            except (soc_error, MBoardProtocolError) as e:
                LOG.error('Interrupted receiving the data from %s:%d, '\
                          'error: %s' % (source+(e,)))
                __disconnect_client(client_socket)
                client_socket = None
                continue

            # Now here we assumen the message contains
            LOG.debug('Received message [%d bytes] '\
                      'from %s:%d' % ((len(m),)+source))
            # Issue MBoard protocol to process the
            # request message (m) send from the client (source)
            r = protocol.server_process(m, source)
            # Try to send the response (r) to client
            # Shutdown the TX pipe of the socket after sending
            try:
                LOG.debug('Processed request for client %s:%d, '\
                          'sending response' % source)
                # Send all data of the response (r)
                tcp_send(client_socket, r)
            except soc_error as e:
                # In case we failed in the middle of transfer we should report error
                LOG.error('Interrupted sending the data to %s:%d, '\
                          'error: %s' % (source+(e,)))
                # ... and close socket
                __disconnect_client(client_socket)
                client_socket = None
                # ... and we should proceed to the others
                continue

            # At this point the request/response sequence is over, we may
            # close the client socket and proceed to the next client
            __disconnect_client(client_socket)
            client_socket=None


        except KeyboardInterrupt as e:
            LOG.debug('Crtrl+C issued ...')
            LOG.info('Terminating server ...')
            break

    # If we were interrupted, make sure client socket is also closed
    if client_socket != None:
        __disconnect_client(client_socket)

    # Close server socket
    __server_socket.close()
    LOG.debug('Server socket closed')
