__author__ = 'aravind'


class UnknownPacketType(Exception):
    pass


class PacketType():
    Announce, AnnounceAck = range(2)

    @classmethod
    def is_pkt_announce(cls, pkt_type):
        return cls.Announce == pkt_type

    @classmethod
    def is_pkt_announce_ack(cls, pkt_type):
        return cls.AnnounceAck == pkt_type


def make_pkt_announce(name=None):
    assert name is not None
    return dict(pkt_type=PacketType.Announce, name=name)


def make_pkt_announce_ack(state=None):
    assert isinstance(state, dict)
    return dict(pkt_type=PacketType.AnnounceAck, state=state)


def decode(data):
    if is_pkt_announce(data):
        return str(data["name"])
    elif is_pkt_announce_ack(data):
        return data["state"]
    else:
        raise UnknownPacketType, "Unable to decode packet {}".format(data)


def is_pkt_announce(data):
    return PacketType.is_pkt_announce(data["pkt_type"])

def is_pkt_announce_ack(data):
    return PacketType.is_pkt_announce_ack(data["pkt_type"])