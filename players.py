__author__ = 'aravind'

from utils.ring_buffer import RingBuffer
from parameters import MAX_PLAYERS


class Players(RingBuffer):
    def __init__(self):
        super(Players, self).__init__()

    def add_player(self, name):
        if self._get_num_objs() < MAX_PLAYERS:
            assert isinstance(name, str)
            self._add_object(name)
        else:
            return "Sorry. Already reached maximum number of players"

    def remove_player(self, name):
        assert isinstance(name, str)
        self._remove_object(name)

    def choose_next_leader(self):
        self._advance_right(1)

    def get_current_leader(self):
        return self._get_head_obj()

    def get_current_order(self):
        return self._objs_to_list()

    def get_num_players(self):
        return self._get_num_objs()

    def get_player(self, index):
        return self._get_obj_at_index(index)

