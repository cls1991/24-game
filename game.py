# coding: utf8

import random

from twisted.internet import (
    protocol, reactor, endpoints
)

from util import make24

CARDS = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10,
         10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13]

HELP = """

  Play 24 point game.

Options:
  --help  Show this message and exit.

Commands:
  start   Start the game.
  commit  Commit your game solution.
  quit    Quit the game.\n
  """

CONNECTIONS = []
CARD_RECORD = {}
SCORE_RECORD = {}
COMMANDS = ('start', 'commit', 'quit')


class GameProtocol(protocol.Protocol):

    def transform_unique_key(self):
        peer = self.transport.getPeer()
        return '{host}:{port}'.format(host=peer.host, port=peer.port)

    def connectionMade(self):
        uk = self.transform_unique_key()
        if uk not in SCORE_RECORD:
            SCORE_RECORD[uk] = 0
        if uk not in CONNECTIONS:
            CONNECTIONS.append(uk)

        self.transport.write(HELP)

    def dataReceived(self, data):
        sp = data.strip().split(' ')
        command = sp[0]
        uk = self.transform_unique_key()
        if command == 'start':
            if uk not in CARD_RECORD:
                cards = random.sample(CARDS, 4)
                CARD_RECORD[uk] = cards
            cards = CARD_RECORD[uk][:]
            for i, c in enumerate(cards):
                cards[i] = str(c)
            response = '{0}\n'.format(' '.join(cards))
        elif command == 'quit':
            response = 'Go to quit game.\n'
        elif command == 'commit':
            if uk not in CARD_RECORD:
                response = 'Type command `start` to generate card numbers first.\n'
            else:
                solution = sp[1]
                correct_answers = make24(CARD_RECORD[uk])
                if solution in correct_answers:
                    SCORE_RECORD[uk] += 1
                    response = 'Congratulations.\n'
                else:
                    if SCORE_RECORD[uk] > 0:
                        SCORE_RECORD[uk] -= 1
                    response = 'Wrong solution.\n'
        else:
            response = 'Unknown command {0}.\n'.format(sp[0])
        self.transport.write(response)
        if command == 'quit':
            self.transport.loseConnection()

    def connectionLost(self, reason=protocol.connectionDone):
        uk = self.transform_unique_key()
        if uk in CONNECTIONS:
            CONNECTIONS.remove(uk)
        if uk in CARD_RECORD:
            CARD_RECORD.pop(uk)
            if SCORE_RECORD[uk] > 0:
                SCORE_RECORD[uk] -= 1


class GameFactory(protocol.Factory):

    def buildProtocol(self, addr):
        return GameProtocol()


endpoints.serverFromString(reactor, 'tcp:1234').listen(GameFactory())
reactor.run()
