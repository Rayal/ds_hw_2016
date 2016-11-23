# Imports----------------------------------------------------------------------
from socket import SHUT_WR, SHUT_RD
from exceptions import Exception
# TCP related constants -------------------------------------------------------
#
DEFAULT_SERVER_PORT = 7777
DEFAULT_SERVER_INET_ADDR = '127.0.0.1'
#
# When receiving big messages in multiple blocks from the TCP stream
# the receive buffer size should be select according to amount of RAM available
# (more RAM = bigger blocks = less receive cycles = faster delivery)
TCP_RECEIVE_BUFFER_SIZE = 1024*1024
MAX_PDU_SIZE = 200*1024*1024 # Reasonable amount of data to store in RAM
# Requests --------------------------------------------------------------------
__REQ_DIR = '1'
__REQ_FILE = '2'
__REQ_EDIT = '3'
__REQ_UPDATE = '4'
__CTR_MSGS = { __REQ_DIR:'Get directory data',
               __REQ_FILE:'Get file',
               __REQ_EDIT:'Edit file',
               __REQ_UPDATE:'File change time'
              }
# Responses--------------------------------------------------------------------
__RSP_OK = '0'
__RSP_BADFORMAT = '1'
__RSP_FILENOTFOUND = '2'
__RSP_UNKNCONTROL = '3'
__RSP_ERRTRANSM = '4'
__RSP_CANT_CONNECT = '5'
__ERR_MSGS = { __RSP_OK:'No Error',
               __RSP_BADFORMAT:'Malformed message',
               __RSP_FILENOTFOUND:'Message not found by iD',
               __RSP_UNKNCONTROL:'Unknown control code',
               __RSP_ERRTRANSM:'Transmission Error',
               __RSP_CANT_CONNECT:'Can\'t connect to server'
               }
# Field separator for sending multiple values ---------------------------------
__MSG_FIELD_SEP = chr(30)
__FILE_SEP = chr(28)
# Exceptions ------------------------------------------------------------------
class FSProtocolError(Exception):
    '''Should be thrown internally on client or server while receiving the
    data, in case remote end-point attempts to not follow the MBoard protocol
    '''
    def __init__(self,msg):
        Exception.__init__(self,msg)
# Common methods --------------------------------------------------------------
def tcp_send(sock,data):
    '''Send data using TCP socket. When the data is sent, close the TX pipe
    @param sock: TCP socket, used to send/receive
    @param data: The data to be sent
    @returns integer,  n bytes sent and error if any
    @throws socket.errror in case of transmission error
    '''
    sock.sendall(data)
    sock.shutdown(SHUT_WR)
    return len(data)

def tcp_receive(sock,buffer_size=TCP_RECEIVE_BUFFER_SIZE):
    '''Receive the data using TCP receive buffer.
    @param buffer_size: integer, the size of the block to receive in one
            iteration of the receive loop
    @returns string, data received
    @throws socket.errror in case of transmission error,
            MBoard PDU size exceeded in case of client attempting to
            send more data the MBoard protocol allows to send in one PDU
            (MBoard request or response) - MAX_PDU_SIZE
    '''
    m = ''      # Here we collect the received message
    # Receive loop
    while 1:
        # Receive one block of data according to receive buffer size
        block = sock.recv(TCP_RECEIVE_BUFFER_SIZE)
        if len(block) <= 0:
            break
        if ( len(m) + len(block) ) >= MAX_PDU_SIZE:
            sock.shutdown(SHUT_RD)
            # Garbage collect the unfinished message (m) and throw exception
            del m
            raise \
                FSProtocolError( \
                    'Remote end-point tried to exceed the MAX_PDU_SIZE'\
                    'of MBoard protocol'\
                )
        # Appending the blocks, assembling the message
        m += block
    return m
