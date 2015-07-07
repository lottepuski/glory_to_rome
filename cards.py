__author__ = 'aravind'

from random import shuffle


class GameOver(Exception):
    pass


class Material(object):
    Wood, Rubble, Concrete, Brick, Marble, Stone = range(6)


class Role(object):
    Craftsman, Laborer, Architect, Legionary, Patron, Merchant = range(6)


class Card(object):
    """ Lazy init routine.
        Must be initialized with
        structure: str,
        material: Material.x,
        role: Role.x,
        value: Int,
        function: str
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            if k == "material":
                setattr(self, k, getattr(Material, v, None))
            elif k == "role":
                setattr(self, k, getattr(Role, v, None))
            else:
                setattr(self, k, v)


class Deck(object):
    def __init__(self):
        self.cards = []
        for x in range(3):
            card = Card(structure="Academy", material="Brick", role="Legionary", value=2,
                        function="May perform one THINKER action after turn during which you performed CRAFTSMAN action")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Amphitheatre", material="Concrete", role="Architect", value=2,
                        function="May perform one CRAFTSMAN action for each INFLUENCE")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Aqueduct", material="Concrete", role="Architect", value=2,
                        function="When performing PATRON action may take client from HAND.  Maximum CLIENTELE x 2")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Archway", material="Brick", role="Legionary", value=2,
                        function="When performing ARCHITECT action may take material from POOL")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Atrium", material="Brick", role="Legionary", value=2,
                        function="When performing MERCHANT action may take from DECK (do not look at card)")
            self.cards.append(card)
        for x in range(6):
            card = Card(structure="Bar", material="Rubble", role="Laborer", value=1,
                        function="When performing PATRON action may take card from DECK")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Basilica", material="Marble", role="Patron", value=3,
                        function="When performing MERCHANT action may take material from HAND")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Bath", material="Brick", role="Legionary", value=2,
                        function="When performing PATRON action each client you hire may perform its action once as it enters CLIENTELE")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Bridge", material="Concrete", role="Architect", value=2,
                        function="When performing LEGIONARY action may take material from STOCKPILE.  Ignore Palisades.  May take from all opponents")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Catacomb", material="Stone", role="Merchant", value=3,
                        function="Game ends immediately.  Score as usual")
            self.cards.append(card)
        for x in range(6):
            card = Card(structure="Circus", material="Wood", role="Craftsman", value=1,
                        function="May play two cards of same role as JACK")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Circus Maximus", material="Stone", role="Merchant", value=3,
                        function="Each client may perform its action twice when you lead or follow its role")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Coliseum", material="Stone", role="Merchant", value=3,
                        function="When performing LEGIONARY action may take opponent's client and place in VAULT as material")
            self.cards.append(card)
        for x in range(6):
            card = Card(structure="Dock", material="Wood", role="Craftsman", value=1,
                        function="When performing LABORER action may take material from HAND")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Forum", material="Marble", role="Patron", value=3,
                        function="One client of each role wins game")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Foundry", material="Brick", role="Legionary", value=2,
                        function="May perform one LABORER action for each INFLUENCE")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Fountain", material="Marble", role="Patron", value=3,
                        function="When performing CRAFTSMAN action may use cards from DECK.  Retain any unused cards in HAND")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Garden", material="Stone", role="Merchant", value=3,
                        function="May perform one PATRON action for each INFLUENCE")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Gate", material="Brick", role="Legionary", value=2,
                        function="Incomplete MARBLE structures provide FUNCTION")
            self.cards.append(card)
        for x in range(6):
            card = Card(structure="Insula", material="Rubble", role="Laborer", value=1,
                        function="Maximum CLIENTELE + 2")
            self.cards.append(card)
        for x in range(6):
            card = Card(structure="Latrine", material="Rubble", role="Laborer", value=1,
                        function="Before performing THINKER action may discard one card to POOL")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Ludus Magna", material="Marble", role="Patron", value=3,
                        function="Each MERCHANT client counts as any role")
            self.cards.append(card)
        for x in range(6):
            card = Card(structure="Market", material="Wood", role="Craftsman", value=1,
                        function="Maximum VAULT + 2")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Palace", material="Marble", role="Patron", value=3,
                        function="May play multiple cards of same role in order to perform additional actions")
            self.cards.append(card)
        for x in range(6):
            card = Card(structure="Palisade", material="Wood", role="Craftsman", value=1,
                        function="Immune to LEGIONARY")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Prison", material="Stone", role="Merchant", value=3,
                        function="May exchange INFLUENCE for opponent's completed structure")
            self.cards.append(card)
        for x in range(6):
            card = Card(structure="Road", material="Rubble", role="Laborer", value=1,
                        function="When adding to STONE structure may use any material")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="School", material="Brick", role="Legionary", value=2,
                        function="May perform one THINKER action for each INFLUENCE")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Scriptorium", material="Stone", role="Merchant", value=3,
                        function="May use one MARBLE material to complete any structure")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Senate", material="Concrete", role="Architect", value=2,
                        function="May take opponent's JACK into HAND at end of turn in which it is played")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Sewer", material="Stone", role="Merchant", value=3,
                        function="May place Orders cards used to lead or follow into STOCKPILE at end of turn")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Shrine", material="Brick", role="Legionary", value=2,
                        function="Maximum HAND + 2")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Stairway", material="Marble", role="Patron", value=3,
                        function="When performing ARCHITECT action may add material to opponent's completed STRUCTURE to make function available to all players")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Statue", material="Marble", role="Patron", value=3,
                        function="+ 3 VP. May place Statue on any SITE")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Storeroom", material="Concrete", role="Architect", value=2,
                        function="All clients count as LABORERS")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Temple", material="Marble", role="Patron", value=3,
                        function="Maximum HAND + 4")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Tower", material="Concrete", role="Architect", value=2,
                        function="May use RUBBLE in any STRUCTURE.  May lay foundation onto any out of town SITE at no extra cost")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Villa", material="Stone", role="Merchant", value=3,
                        function="When performing ARCHITECT action may complete Villa with one material")
            self.cards.append(card)
        for x in range(3):
            card = Card(structure="Vomitorium", material="Concrete", role="Architect", value=2,
                        function="Before performing THINKER action may discard all cards to POOL")
            self.cards.append(card)
        self.shuffle()

    def shuffle(self):
        shuffle(self.cards)

    def get_n_cards(self, n):
        cards = []
        for i in xrange(n):
            try:
                cards.append(self.cards.pop())
            except IndexError:
                raise GameOver, "Last card in deck has been drawn"
        return cards
