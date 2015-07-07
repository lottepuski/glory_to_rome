__author__ = 'aravind'


class UnknownPacketType(Exception):
    pass


class PacketType():
    Announce, AnnounceAck, Declare, DeclareAck, \
    Act, ActAck = range(6)

    @classmethod
    def is_pkt_announce(cls, pkt_type):
        return cls.Announce == pkt_type

    @classmethod
    def is_pkt_announce_ack(cls, pkt_type):
        return cls.AnnounceAck == pkt_type

    @classmethod
    def is_pkt_declare(cls, pkt_type):
        return cls.Declare == pkt_type

    @classmethod
    def is_pkt_declare_ack(cls, pkt_type):
        return cls.DeclareAck == pkt_type

    @classmethod
    def is_pkt_act(cls, pkt_type):
        return cls.Act == pkt_type

    @classmethod
    def is_pkt_act_ack(cls, pkt_type):
        return cls.ActAck == pkt_type


def make_pkt_announce(name=None):
    assert name is not None
    return dict(pkt_type=PacketType.Announce, name=name)


def make_pkt_announce_ack(state=None):
    assert isinstance(state, dict)
    return dict(pkt_type=PacketType.AnnounceAck, state=state)


def make_pkt_declare(name=None, card=None):
    assert name is not None
    assert isinstance(card, dict)
    return dict(pkt_type=PacketType.Declare, name=name, card=card)


def make_pkt_declare_ack(state=None):
    assert isinstance(state, dict)
    return dict(pkt_type=PacketType.DeclareAck, state=state)


def make_pkt_act(name=None, actions=None):
    assert name is not None
    assert isinstance(actions, dict)
    return dict(pkt_type=PacketType.Act, name=name, actions=actions)


def make_pkt_act_ack(state=None):
    assert isinstance(state, dict)
    return dict(pkt_type=PacketType.ActAck, state=state)


def decode(data):
    if is_pkt_announce(data):
        return str(data["name"])
    elif is_pkt_announce_ack(data):
        return data["state"]
    elif is_pkt_declare(data):
        return data["name"], data["card"]
    elif is_pkt_declare_ack(data):
        return data["state"]
    elif is_pkt_act(data):
        return data["name"], data["actions"]
    elif is_pkt_act_ack(data):
        return data["state"]
    else:
        raise UnknownPacketType, "Unable to decode packet {}".format(data)


def is_pkt_announce(data):
    # assert isinstance(data, dict) and data.has_key("pkt_type")
    return PacketType.is_pkt_announce(data["pkt_type"])


def is_pkt_announce_ack(data):
    # assert isinstance(data, dict) and data.has_key("pkt_type")
    return PacketType.is_pkt_announce_ack(data["pkt_type"])


def is_pkt_declare(data):
    # assert isinstance(data, dict) and data.has_key("pkt_type")
    return PacketType.is_pkt_declare(data["pkt_type"])


def is_pkt_declare_ack(data):
    # assert isinstance(data, dict) and data.has_key("pkt_type")
    return PacketType.is_pkt_declare_ack(data["pkt_type"])


def is_pkt_act(data):
    # assert isinstance(data, dict) and data.has_key("pkt_type")
    return PacketType.is_pkt_act(data["pkt_type"])


def is_pkt_act_ack(data):
    # assert isinstance(data, dict) and data.has_key("pkt_type")
    return PacketType.is_pkt_act_ack(data["pkt_type"])
