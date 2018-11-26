import random
from collections import namedtuple

Card = namedtuple('Card', ['value', 'suit'])


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

    def drawCard(self):
        return self.cards.pop() #removes the last card ("the top")

class Player(object):
    def __init__(self, name):
        self.hand = []
        self.name = name

    def __str__(self):
        return str(self.name)

    def draw(self, game):
        """
        Draws from the current game
        """
        self.hand.append(game.drawCard())
    
    # gives a card back to a player
    def takeCard(self, card):
        self.hand.append(card)

    # it occurs to me now that this probably isn't the best way to pass cards
    def playCard(self, card, game):
        """
        removes and returns card if successful, None if fails
        """
        try:
            self.remove(card)
            return card
        except:
            return None
    
    def showHand(self):
        for card in self.hand:
            print(card)
            
    def clearHand(self, deck=None):
        """
        If there is a deck, return the card to it.
        Else, simply clear the hand
        """
        if (deck == None):
            self.hand = []
        else:
            for card in self.hand:
                deck.append(card)

class History(object):
    def __init__(self):
        self.moves = []

    def recordMove(self, player, card, result):
        self.moves.append((player, card, result))

                
    
    
    
    
    
    
#
