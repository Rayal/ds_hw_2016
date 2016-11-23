# Implements file system protocol on TCP (server-side)
# in this protocol clients can edit plaintext files (delivered by TCP)
#------------------------------------------------------------------------------

# Setup Python logging --------------------------------------------------------
import logging
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG,format=FORMAT)
LOG = logging.getLogger()
# Imports----------------------------------------------------------------------
from tcp.common import __RSP_BADFORMAT,\
     __REQ_DIR, __MSG_FIELD_SEP, __RSP_OK, __REQ_EDIT,\
     __REQ_FILE, __RSP_FILENOTFOUND, __RSP_UNKNCONTROL
from socket import error as soc_err
import tcp.server.fileservice as fs

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

def server_process(message,source):
    '''Process the client's message, modify the board if needed
        @param message: string, protocol data unit received from client
        @param source: tuple ( ip, port ), client's socket address
        @returns string, response to send to client
    '''

    LOG.debug('Received request [%d bytes] in total' % len(message))

    LOG.debug('Request control code (%s)' % message[0])

    if message.startswith(__REQ_EDIT + __MSG_FIELD_SEP):
        msg = message[2:].split(__MSG_FIELD_SEP)
        LOG.debug('Client %s:%d will edit file %s ' % (source+(msg[0],)))
        m_id = fs.change_file(msg[0], msg[1])
        if m_id == 0:
            LOG.info('Successfully edited file %s' % msg[0])
            return __RSP_OK
        LOG.error("Unable to edit file %s" % msg[0])
        return __RSP_FILENOTFOUND

    elif message.startswith(__REQ_DIR):
        LOG.debug('New directory content request from %s:%d.'%source)
        ret = fs.get_dir()
        return __MSG_FIELD_SEP.join((__RSP_OK,)+(ret,))

    elif message.startswith(__REQ_FILE + __MSG_FIELD_SEP):
        s = message[2:]
        LOG.debug('New file request from %s:%d: %s' % (source+(s,)))
        m = fs.get_file(s)
        if m == None:
            LOG.debug('No such file: %s' % s)
            return __RSP_FILENOTFOUND
        #m = map(str,m)
        return __MSG_FIELD_SEP.join((__RSP_OK,)+(m,))

    else:
        LOG.debug('Unknown control message received: %s ' % message)
        return __RSP_UNKNCONTROL
