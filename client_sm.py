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

    def declare(self):
        card = self.pick_card()
        if card:
            data = self.client.declare(card=card)
            state = decode(data)
            if state is not None:
                self.parse_state(state)
            else:
                print "something is wrong. state is none"
            self.show_state()

    def pick_card(self):
        if self.is_current_leader:
            return self.__state["hand"][0]
        for card in self.__state["hand"]:
            if card["role"] == self.current_role:
                return card

    def show_state(self):
        if self.__state is None:
            print "state has not been initialized"
            return
        self.pp.pprint(self.__state)

    def parse_state(self, state):
        self.is_current_leader = state["is_current_leader"]
        self.current_role = state["current_role"]
        self.__state = {}
        self.__parse_object(state, "card_in_play")
        self.__parse_iterable(state, "hand")
        self.__parse_iterable(state, "clients")
        self.__parse_iterable(state, "stockpile")

    def __parse_object(self, obj, key):
        tmp_obj = obj.pop(key)
        if tmp_obj:
            self.__state[key] = vars(tmp_obj)

    def __parse_iterable(self, obj, key):
        tmp_obj = obj.pop(key)
        t = []
        for card in tmp_obj:
            t.append(vars(card))
        self.__state[key] = t
