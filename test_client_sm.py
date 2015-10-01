__author__ = 'aravind'
from unittest import TestCase
from client_sm import GameClient

amara = GameClient("amara")
amara.announce()
amara.declare()

bhramara = GameClient("bhramara")
bhramara.announce()
bhramara.declare()


class TestGameManager(TestCase):
    def test_announce(self):
        assert True
