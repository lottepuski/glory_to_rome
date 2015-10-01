__author__ = 'aravind'

import copy
from utils.ring_buffer import RingBuffer
from parameters import MAX_PLAYERS
from cards import Card, Deck, GameOver


class UnknownPlayerException(Exception):
    pass


class Player(object):
    def __init__(self, name):
        self.name = name
        self.influence = 2
        self.hand_size = 5
        self.stockpile = []
        self.vault = []
        self.clients = []
        self.projects = []
        self.powers = []
        self.hand = []
        self.card_in_play = None

    def __repr__(self):
        ''' We can not use vars because of hidden values
        :return: dictionary of public variables + player's hand
        '''
        val = copy.deepcopy(vars(self))
        val.pop("vault")
        return val

    def public_view(self):
        ''' Return player's state to other players
        :return:
        '''
        val = copy.deepcopy(vars(self))
        val.pop("vault")
        val.pop("hand")
        return val

    def add_to_hand(self, cards):
        self.hand.extend(cards)


class Players(RingBuffer):
    ''' Players is the general purpose class that holds the all data relating
        to players and the game.
    '''

    def __init__(self):
        super(Players, self).__init__()
        self.__players_map = dict()
        self.deck = Deck()

    def add_player(self, name):
        if self._get_num_objs() < MAX_PLAYERS:
            assert isinstance(name, str)
            self._add_object(name)
            player = Player(name)
            player.add_to_hand(self.deck.get_n_cards(player.hand_size))
            self.__players_map[name] = player
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

    def get_player_by_name(self, name):
        return self.__players_map[name]

    def add_card_to_hand(self, name, card):
        '''
        :param name:
        :param card:
        :return: True or False
        '''
        # assert isinstance(name, str) and self.__players_map.has_key(name)
        player = self.get_player_by_name(name)
        if len(player.hand) < player.hand_size:
            player.hand.append(card)
            return True
        return False

    def get_current_state(self, name):
        try:
            player = self.get_player_by_name(name)
        except KeyError:
            raise UnknownPlayerException, "Player not found"

        return player.__repr__()

    def bring_card_to_play(self, name, card):
        '''
        :param card: dict
        :return: None
        '''
        player = self.get_player_by_name(name)
        print player.name
        for i, x in enumerate(player.hand):
            if x.equal(card):
                player.card_in_play = player.hand.pop(i)
