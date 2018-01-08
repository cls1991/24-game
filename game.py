# coding: utf8

import sys

from twisted.internet import (
    protocol, reactor, endpoints
)
from twisted.python import log

from util import (
    make24, generate_cards
)

RANK_LENGTH = 3
DEFAULT_IP = '127.0.0.1'

HELP = """
  Play 24 point game.
  
Commands:
  start   Start the game.
  submit  Commit your guess(yes/y for solutions, others for no solutions).
  rank    Show the first three of score rank.
  info    Show player info.
  quit    Quit the game.
  help    Show this message.

"""

CONNECTIONS = {}
CARD_RECORD = {}
SCORE_RECORD = {}
SCORE_RANKS = []


class GameProtocol(protocol.Protocol):

    def __init__(self):
        pass

    def transform_host_key(self):
        peer = self.transport.getPeer()
        return peer.host

    def transform_peer_key(self):
        peer = self.transport.getPeer()
        return '{host}:{port}'.format(host=peer.host, port=peer.port)

    def connectionMade(self):
        hk = self.transform_host_key()
        if hk in CONNECTIONS:
            self.transport.write('Multi login is not allowed!\n')
            self.transport.loseConnection()
        else:
            log.msg('Received connection from {0}'.format(hk))
            pk = self.transform_peer_key()
            CONNECTIONS[hk] = pk
            if hk not in SCORE_RECORD:
                SCORE_RECORD[hk] = 0
                message = 'Welcome, type command `help` for more details.\n'
            else:
                message = 'Type command `start` to play game, have fun!\n'
            self.transport.write(message)

    def dataReceived(self, data):
        sp = data.strip().split(' ')
        command = sp[0]
        hk = self.transform_host_key()
        if command == 'start':
            if hk not in CARD_RECORD:
                cards = generate_cards()
                CARD_RECORD[hk] = cards
            cards = CARD_RECORD[hk][:]
            for i, c in enumerate(cards):
                cards[i] = str(c)
            response = '{0}\n'.format(' '.join(cards))
        elif command == 'quit':
            response = 'Bye~\n'
        elif command == 'submit':
            if hk not in CARD_RECORD:
                response = 'Type command `start` to generate card numbers first.\n'
            else:
                guess = False
                if len(sp) > 1:
                    if sp[1].lower() in ('yes', 'y'):
                        guess = True
                solution = make24(CARD_RECORD[hk])
                if (guess and solution) or (not guess and not solution):
                    SCORE_RECORD[hk] += 1
                    response = 'Congratulations.\n'
                else:
                    if SCORE_RECORD[hk] > 0:
                        SCORE_RECORD[hk] -= 1
                    response = "You're wrong, one of the solutions is `{0}`.\n".format(solution) if solution \
                        else "You're wrong, no solutions!\n"
                CARD_RECORD.pop(hk)
        elif command == 'rank':
            scores = [str(s) for s in SCORE_RANKS]
            response = 'Score ranks: {0}.\n'.format(' '.join(scores))
        elif command == 'info':
            response = 'Your connection is {0}, your score is {1}.\n'.format(CONNECTIONS[hk], SCORE_RECORD[hk])
        elif command == 'GET':
            if hk == DEFAULT_IP:
                s = sorted(SCORE_RECORD.values(), reverse=True)
                ll = RANK_LENGTH if len(s) > RANK_LENGTH else len(s)
                for x in range(ll):
                    SCORE_RANKS.append(s[x])
                for x in range(RANK_LENGTH - ll):
                    SCORE_RANKS.append(SCORE_RANKS[-1])
                SCORE_RECORD.clear()
                response = 'Successful refresh score ranks.\n'
            else:
                response = 'External invoke is not allowed!\n'
        elif command == 'help':
            response = HELP
        else:
            response = 'Unknown command {0}.\n'.format(sp[0])
        self.transport.write(response)
        if command == 'quit':
            self.transport.loseConnection()

    def connectionLost(self, reason=protocol.connectionDone):
        hk = self.transform_host_key()
        if hk in CONNECTIONS:
            pk = self.transform_peer_key()
            if CONNECTIONS[hk] == pk:
                CONNECTIONS.pop(hk)
                if hk in CARD_RECORD:
                    CARD_RECORD.pop(hk)
                    if hk in SCORE_RECORD and SCORE_RECORD[hk] > 0:
                        SCORE_RECORD[hk] -= 1


class GameFactory(protocol.Factory):

    def __init__(self):
        pass

    def buildProtocol(self, addr):
        return GameProtocol()


log.startLogging(sys.stdout)
endpoints.serverFromString(reactor, 'tcp:12345').listen(GameFactory())
reactor.run()
