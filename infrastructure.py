import random
from collections import namedtuple

Card = namedtuple('Card', ['value', 'suit'])

# rule settings
Rule = namedtuple('Rule', ['rule', 'setting'])
BASICVALUE = 1
BASICSUIT = 2 # I don't think there's much we can do with this as of now
WILDVALUE = 3
WILDSUIT = 4

#notification types
Notification = namedtuple('Notification', ['type', 'attemptedCard', 'lastCard'])

LEGAL = 1
PENALTY = 2
WON = 3


class Deck(object):
    def __init__(self):
        self.cards = []
        self.build()
        self.shuffle()

    def build(self):
        """
        Initializes the deck with a fresh set of cards
        """
        self.cards = []
        for s in ["D", "H", "S", "C"]:
            for v in range(2,15):
                self.cards.append(Card(value=v,suit=s))

    def shuffle(self):
        random.shuffle(self.cards)

    # returns a card if the deck is not empty, None if it is empty
    def drawCard(self):
        if len(self.cards) == 0:
            return None
        else:
            return self.cards.pop() #removes the last card ("the top")
    
    
# keeps track of a bunch of round histories
class GameHistory(object):
    def __init__(self):
        self.rounds = []

    def addRound(self, roundHistory):
        self.rounds.append(roundHistory)

# keeps track of the history of a round. further indices are more recent games
class RoundHistory(object):
    def __init__(self):
        self.moves = []

    def recordMove(self, notification):
        self.moves.append(copy.deepcopy(notification)) # watch out. I have a feeling this will slow down things considerably



    
    
    
    
    
#
