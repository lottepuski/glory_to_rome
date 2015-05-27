__author__ = 'aravind'
from state_machine import Machine
from players import Players


class GameManager(object):
    def __init__(self):
        self.players = Players()
        self.curr_player = 0
        self.curr_card = None
        self.curr_roles = []

    def add_players(self, names):
        assert isinstance(names, list)
        for x in names:
            self.players.add_player(x)

    def choose_next_leader(self):
        self.players.choose_next_leader()
        self.curr_player = 0

    def is_end_of_round(self):
        return self.curr_player == self.players.get_num_players() - 1

    def go_to_next_player(self):
        if not self.is_end_of_round():
            self.curr_player += 1
        else:
            self.curr_player = 0

    def validate_think(self, e):
        msg1 = '{} has decided to think with a {}. {} will lead the next round'
        msg2 = '{} has decided to think with a {}. Waiting for {}'
        msg3 = '{} has decided to think with a {}. Will start actions'
        if self.curr_player == 0 and self.can_get_requested_card(e):
            curr_player = self.players.get_player(0)
            next_player = self.players.get_player(1)
            print msg1.format(curr_player, e.card, next_player)
        elif not self.is_end_of_round() and self.can_get_requested_card(e):
            curr_player = self.players.get_player(self.curr_player)
            next_player = self.players.get_player(self.curr_player + 1)
            self.curr_roles.append("Think_" + e.card)
            print msg2.format(curr_player, e.card, next_player)
        elif self.can_get_requested_card(e):
            curr_player = self.players.get_player(self.curr_player)
            self.curr_roles.append("Think_" + e.card)
            print msg3.format(curr_player, e.card)

    def handle_thinker(self, e):
        if e.src == "round_begin":
            self.validate_think(e)
            self.choose_next_leader()
            e.dst = "round_begin"
        elif e.src == "round_middle" and not self.is_end_of_round():
            self.validate_think(e)
            self.go_to_next_player()
            e.dst = "round_middle"
        else:
            self.validate_think(e)
            self.go_to_next_player()
            print "Actions expected in this round : {}".format(self.curr_roles)
            e.dst = "actions_begin"
        return e.dst

    def validate_declare(self, e):
        print "{} has declared the card {}".format(
            self.players.get_player(self.curr_player), e.card)
        if not self.can_accept(e.card):
            print "Invalid declaration"

    def handle_card_declare(self, e):
        if e.src == "round_begin":
            self.validate_declare(e)
            e.dst = "round_middle"
        elif e.src == "round_middle" and not self.is_end_of_round():
            self.validate_declare(e)
            e.dst = "round_middle"
        else:
            self.validate_declare(e)
            print "Actions expected in this round : {}".format(self.curr_roles)
            e.dst = "actions_begin"
        return e.dst

    def handle_action(self, e):
        if e.src == "actions_begin":
            self.go_to_next_player()
            e.dst = "actions_middle"
        elif e.src == "actions_middle" and not self.is_end_of_round():
            self.go_to_next_player()
            e.dst = "actions_middle"
        else:
            self.choose_next_leader()
            e.dst = "round_begin"
        return e.dst

    def can_accept(self, card):
        if self.curr_player == 0:
            self.curr_card = card
            self.curr_roles.append(card)
            self.go_to_next_player()
            return True
        elif self.curr_card == card:
            self.curr_roles.append(card)
            self.go_to_next_player()
            return True
        return False

    @staticmethod
    def can_get_requested_card(e):
        return True


manager = GameManager()
manager.add_players(['amara', 'bhramara', 'chamara', "dilbara"])


def run_round(e):
    if e.event == "think":
        return manager.handle_thinker(e)
    elif e.event == "declare_card":
        return manager.handle_card_declare(e)
    elif e.event == "perform_act":
        return manager.handle_action(e)


server_fsm = {
    "initial": "round_begin",
    "events": [
        {
            "action": "think",
            "src": [
                "round_begin",
                "round_middle"
            ],
            "dst": [
                "round_begin",
                "round_middle",
                "actions_begin"
            ],
        },
        {
            "action": "declare_card",
            "src": [
                "round_begin",
                "round_middle"
            ],
            "dst": [
                "round_middle",
                "actions_begin"
            ],
        },
        {
            "action": "perform_act",
            "src": [
                "actions_begin",
                "actions_middle"
            ],
            "dst": [
                "actions_middle",
                "round_begin"
            ],
        }
    ],
    "callbacks": {
        "on_event": run_round,
        # "ondeclare_card": run_round,
        # "onperform_act": run_round,
    }
}


def server_sm():
    sm = Machine(server_fsm)
    return sm


if __name__ == "__main__":
    sm = server_sm()
    print "Current", sm.current
    # sm._enter_state = run_round
    print manager.players.get_current_order()
    sm.think(card="Jack")
    print "Current", sm.current
    print manager.players.get_current_order()
    print "Current", sm.current
    sm.think(card="Card")
    print manager.players.get_current_order()
    sm.declare_card(card="Patron")
    sm.declare_card(card="Patron")
    sm.declare_card(card="Patron")
    sm.think(card="Jack")