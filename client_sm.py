__author__ = 'aravind'

from communications.gameclient import Client
from communications.game_protocol import *
from state_machine.machine import Machine
import pprint
from collections import OrderedDict

class GameClient(object):
    def __init__(self, name):
        self.client = Client(name)
        self.name = name
        self.init_state_machine()
        self.__state = None
        self.curr_state = ""
        self.pp = pprint.PrettyPrinter(indent=4)

    def init_state_machine(self):
        _initial = "created"
        _events = [
            {
                "action": "start",
                "src": "created",
                "dst": "declare_action",
                "callbacks": dict(on_event=self.announce)
            }
        ]
        _fsm = dict(initial=_initial, events=_events)
        self.sm = Machine(_fsm)

    def announce(self):
        data = self.client.announce()
        state = decode(data)
        if state is not None:
            self.parse_state(state)
        else:
            print "something is wrong. state is none"
        self.show_state()

    def show_state(self):
        if self.__state is None:
            print "state has not been initialized"
            return
        self.pp.pprint(self.__state)

    def parse_state(self, state):
        self.__state = {}
        self.__parse_obj(state, "hand")
        self.__parse_obj(state, "clients")
        self.__parse_obj(state, "stockpile")


    def __parse_obj(self, obj, key):
        tmp_obj = obj.pop(key)
        t = []
        for card in tmp_obj:
            t.append(vars(card))
        self.__state[key] = t
