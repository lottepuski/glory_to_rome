#!/usr/bin/python

from clish import InteractiveCommand, InteractiveShell
from client_sm import GameClient

class Application(object):
    def __init__(self):
        self.client = GameClient("amara")
        self.client.announce()

    def run(self):
        shell = InteractiveShell(banner="Welcome to GTR v0.1", prompt="GTR> ")
        declare = Declare(self.client)
        add = AddCard(self.client)
        show = Display(self.client)
        shell.add_command(show)
        shell.add_command(declare)
        shell.add_command(add)
        shell.run()

class Display(InteractiveCommand):
    def __init__(self, client):
        self.client = client
        super(Display, self).__init__()

    def get_name(self):
        return 'display'

    def get_options(self):
        return { }

    def handle_command(self, opts=None, args=None):
        self.client.show_state()

    def get_short_description(self):
        return 'Show current player state'

    def get_help_message(self):
        return 'display'

class Declare(InteractiveCommand):
    def __init__(self, client):
        self.client = client
        super(Declare, self).__init__()

    def get_name(self):
        return 'declare'

    def get_options(self):
        return { }

    def handle_command(self, opts=None, args=None):
        print args

    def get_short_description(self):
        return 'Declare a card. Use 3 cards of the same role as Jack'

    def get_help_message(self):
        return 'declare card1 card2'

class AddCard(InteractiveCommand):
    def __init__(self, client):
        self.client = client
        super(AddCard, self).__init__()

    def get_name(self):
        return 'add'

    def get_options(self):
        return { }

    def handle_command(self, opts=None, args=None):
        print opts, args

    def get_short_description(self):
        return 'Add card(s) to an existing structure'

    def get_help_message(self):
        return 'add structure card1 ...'

def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()