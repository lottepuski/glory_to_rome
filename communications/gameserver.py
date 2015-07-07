#!/usr/bin/env python

import select
import socket
import sys
import signal
from sock_utils import send, receive
from game_protocol import *

BUFSIZ = 1024


class GameServer(object):
    """ Simple chat server using select """

    def __init__(self, port=3490, backlog=5, handler=None):
        self.num_players = 0
        # Client map
        self.player_map = {}
        # Output socket list
        self.outputs = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('', port))
        # print 'Listening to port', port
        self.server.listen(backlog)
        # Trap keyboard interrupts
        signal.signal(signal.SIGINT, self.signal_handler)
        assert handler is not None, "What must I do with all these messages?"
        self.msg_handler = handler

    def signal_handler(self, signum, frame):
        """
        Close the server
        :param signum:
        :param frame:
        """
        print 'Shutting down server...'
        # Close existing client sockets
        for o in self.outputs:
            o.close()

        self.server.close()

    def get_name(self, client):
        """
        Return the printable name of the client, given its socket...
        :param client:
        :return:
        """
        return self.player_map[client]

    def send(self, to, msg):
        flag = False
        for x in self.outputs:
            if self.get_name(x) == to:
                send(x, msg)
                flag = True
                break
        if not flag:
            print "unable to find player {}".format(to)

    def serve(self):
        """ Main loop
        """
        inputs = [self.server, sys.stdin]
        self.outputs = []

        running = 1

        while running:
            try:
                input_ready, output_ready, except_ready = select.select(inputs, self.outputs, [])
            except select.error, e:
                break
            except socket.error, e:
                break

            for s in input_ready:
                if s == self.server:
                    # handle the server socket
                    client_socket, address = self.server.accept()
                    # address = ip address
                    print 'Server: got connection {0:d} from {1:s}'.format(client_socket.fileno(), address)
                    # Read the announce packet
                    data = receive(client_socket)
                    name = decode(data)
                    self.player_map[client_socket] = name
                    self.num_players += 1
                    self.outputs.append(client_socket)
                    inputs.append(client_socket)
                    announce_ack = self.msg_handler(data)
                    self.send(name, announce_ack)

                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0
                else:
                    # handle all other sockets
                    try:
                        data = receive(s)
                        if data:
                            # Send as new client's message...
                            print data
                            msg = self.msg_handler(data)
                            send(s, msg)
                        else:
                            print 'Server: %d hung up' % s.fileno()
                            self.num_players -= 1
                            s.close()
                            inputs.remove(s)
                            self.outputs.remove(s)

                            # Send client leaving information to others
                            msg = '\n(Hung up: Client from {0:s})'.format(self.get_name(s))
                            for o in self.outputs:
                                # o.send(msg)
                                send(o, msg)

                    except socket.error, e:
                        # Remove
                        inputs.remove(s)
                        self.outputs.remove(s)
        # Cleanup
        self.server.close()


if __name__ == "__main__":
    GameServer().serve()
