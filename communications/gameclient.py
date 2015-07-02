#! /usr/bin/env python
#############################################################################
# The chat client
#############################################################################

"""
Simple chat client for the chat server. Defines
a simple protocol to be used with chatserver.

"""

import socket
import sys
import select
from sock_utils import send, receive
from game_protocol import *

SERVER = '127.0.0.1'
PORT = 3490
BUFSIZ = 1024


class Client(object):
    """ A simple command line chat client using select """

    def __init__(self, name, host=SERVER, port=PORT):
        """
        :rtype : None
        """
        self.name = name
        # Quit flag
        self.flag = False
        self.port = int(port)
        self.host = host
        # Initial prompt
        self.prompt = '@'.join((name, socket.gethostname().split('.')[0])) + ': '
        # Connect to server at port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, self.port))
        except socket.error, e:
            print 'Could not connect to chat server @%d' % self.port
            sys.exit(1)

    def cmdloop(self):
        while not self.flag:
            try:
                sys.stdout.write(self.prompt)
                sys.stdout.flush()

                # Wait for input from stdin & socket
                input_ready, output_ready, except_ready = \
                    select.select([0, self.sock], [], [])

                for i in input_ready:
                    if i == 0:
                        data = sys.stdin.readline().strip()
                        c_data = {'data': data}
                        if data: send(self.sock, c_data)
                    elif i == self.sock:
                        data = receive(self.sock)
                        if not data:
                            print 'Shutting down.'
                            self.flag = True
                            break
                        else:
                            sys.stdout.write(data + '\n')
                            sys.stdout.flush()

            except KeyboardInterrupt:
                print 'Interrupted.'
                self.sock.close()
                break

    def send(self, data):
        send(self.sock, data)

    def announce(self):
        pkt = make_pkt_announce(self.name)
        self.send(pkt)
        return receive(self.sock)

if __name__ == "__main__":
    name = sys.argv[1]
    server = (SERVER, sys.argv[2])[len(sys.argv) >= 3]
    port = (PORT, sys.argv[3])[len(sys.argv) >= 4]
    client = Client(name, server, port)
    client.cmdloop()
