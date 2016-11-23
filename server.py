# Imports----------------------------------------------------------------------
from tcp.server.main import mboard_server_main
from tcp.common import DEFAULT_SERVER_INET_ADDR,\
    DEFAULT_SERVER_PORT
from argparse import ArgumentParser # Parsing command line arguments
from sys import path,argv
from os.path import abspath, sep
# Main method -----------------------------------------------------------------
if __name__ == '__main__':
    # Find the script absolute path, cut the working directory
    a_path = sep.join(abspath(argv[0]).split(sep)[:-1])
    # Append script working directory into PYTHONPATH
    path.append(a_path)
    # Parsing arguments
    parser = ArgumentParser()
    parser.add_argument('-l','--listenaddr', \
                        help='Bind server socket to INET address, '\
                        'defaults to %s' % DEFAULT_SERVER_INET_ADDR, \
                        default=DEFAULT_SERVER_INET_ADDR)
    parser.add_argument('-p','--listenport', \
                        help='Bind server socket to UDP port, '\
                        'defaults to %d' % DEFAULT_SERVER_PORT, \
                        default=DEFAULT_SERVER_PORT)
    args = parser.parse_args()

    mboard_server_main(args)
