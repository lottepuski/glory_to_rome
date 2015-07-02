###############################################################################
# The communication module (sock_utils.py)
###############################################################################
import json
import jsonpickle
import socket
import struct

# marshall = json.dumps
# unmarshall = json.loads

marshall = jsonpickle.encode
unmarshall = jsonpickle.decode

def send(channel, *args):
    buf = marshall(args)
    value = socket.htonl(len(buf))
    size = struct.pack("L", value)
    channel.send(size)
    channel.send(buf)

def receive(channel):
    size = struct.calcsize("L")
    size = channel.recv(size)
    try:
        size = socket.ntohl(struct.unpack("L", size)[0])
    except struct.error, e:
        return ''

    buf = ""

    while len(buf) < size:
        buf = channel.recv(size - len(buf))

    return unmarshall(buf)[0]