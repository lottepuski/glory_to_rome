__author__ = 'aravind'
from unittest import TestCase
from client_sm import GameClient

client = GameClient("amara")
client.announce()
client.declare()


class TestGameManager(TestCase):
    def test_announce(self):
        assert True
