# Implements message board protocol on TCP (server-side)
# in this protocol client's can send a big messages (delivered by TCP)
# Therefore there is no need to additionally implement sessions.
#
# Also as we can now send big messages we do no need to split the
# "get last N messages" routine into 2 sub routines, like we did for UDP.
#
# Client(c) <-----------> Server requests/responses
#
#   publish(M) --0:M---->|
#      |                 | mboard.put(M,c)
#      | <------OK-------|
#
#   last(N) ---1:N------>|
#      |                 | if int(N):
#      |                 |     iDs = mboard.last(N)
#      | <----- iDs -----|     msgs = map(mboard.get, iDs)
#      | <-----ERR-------| else
#
#------------------------------------------------------------------------------
'''
MBoard Protocol Server-Side (TCP)
Created on Aug 19, 2016

@author: devel
'''
# Setup Python logging --------------------------------------------------------
import logging
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG,format=FORMAT)
LOG = logging.getLogger()
# Imports----------------------------------------------------------------------
from exceptions import ValueError # for handling number format exceptions
from tcp.mboard.sessions.common import __RSP_BADFORMAT,\
     __REQ_DIR, __MSG_FIELD_SEP, __RSP_OK, __REQ_EDIT,\
     __REQ_FILE, __RSP_FILENOTFOUND, __RSP_UNKNCONTROL
from socket import error as soc_err
import tcp.mboard.sessions.server.fileservice as fs
# Constants -------------------------------------------------------------------
___NAME = 'MBoard Protocol'
___VER = '0.1.0.0'
___DESC = 'State-less Message Board Protocol Server-Side (TCP version)'
___BUILT = '2016-08-23'
___VENDOR = 'Copyright (c) 2016 DSLab'
# Static functions ------------------------------------------------------------
def __disconnect_client(sock):
    '''Disconnect the client, close the corresponding TCP socket
    @param sock: TCP socket to close (client socket)
    '''

    # Check if the socket is closed disconnected already ( in case there can
    # be no I/O descriptor
    try:
        sock.fileno()
    except soc_err:
        LOG.debug('Socket closed already ...')
        return

    # Closing RX/TX pipes
    LOG.debug('Closing client socket')
    # Close socket, remove I/O descriptor
    sock.close()
    LOG.info('Disconnected client')

def server_process(board,message,source,oldprotocol=False):
    '''Process the client's message, modify the board if needed
        @param board: active message board (static lib.)
        @param message: string, protocol data unit received from client
        @param source: tuple ( ip, port ), client's socket address
        @param oldprotocol: backward compatibility flag (for 0.0.0.x clients)
        @returns string, response to send to client
    '''

    LOG.debug('Received request [%d bytes] in total' % len(message))
    if len(message) < 2:
        LOG.degug('Not enough data received from %s ' % message)
        return __RSP_BADFORMAT
    LOG.debug('Request control code (%s)' % message[0])

    if message.startswith(__REQ_EDIT + __MSG_FIELD_SEP):
        msg = message[2:]
        LOG.debug('Client %s:%d will edit file %s ' % (source+(msg[-2],)))
        m_id = fs.change_file(msg[-2], msg[-1])
        if m_id == 0:
            LOG.info('Successfully edited file %s' % msg[-2])
            return __RSP_OK
        LOG.error("Unable to edit file %s" % msg[-2])
        return __RSP_FILENOTFOUND

    elif message.startswith(__REQ_DIR + __MSG_FIELD_SEP):
        s = message[2:]
        LOG.debug('New directory content request from %s:%d: '% (source+(s[-1],)))
        ret = map(str,fs.get_dir())
        return __MSG_FIELD_SEP.join((__RSP_OK,)+tuple(ret))

    elif message.startswith(__REQ_FILE + __MSG_FIELD_SEP):
        s = message[2:]
        LOG.debug('New file request from %s:%d: %s' % (source+s[-1]))
        m = fs.get_file(s[-1])
        if m == None:
            LOG.debug('No such file: %s' % s[-1])
            return __RSP_FILENOTFOUND
        m = map(str,m)
        return __MSG_FIELD_SEP.join((__RSP_OK,)+tuple(m))

    else:
        LOG.debug('Unknown control message received: %s ' % message)
        return __RSP_UNKNCONTROL
