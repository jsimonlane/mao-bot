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

    # returns a card if the deck is not empty, None if it is empty
    def drawCard(self):
        if len(self.cards) == 0:
            return None
        else:
            return self.cards.pop() #removes the last card ("the top")
    
class Player(object):
    def __init__(self, name):
        self.hand = []
        self.name = name

    def __str__(self):
        return str(self.name)
    
    # gives a card back to a player
    def takeCard(self, card):
        self.hand.append(card)
    
    def showHand(self):
        for card in self.hand:
            print(card)
        
    def won(self):
        return len(self.hand) == 0
            
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
                
    # removes and returns a card
    def takeAction(self):
        card = self.chooseCard()
        self.hand.remove(card)
        return card
        
        
    #AI METHOD HERE
    # notified when the state of the game changes, allows for analysis opportunity
    def notify(self, action):
        pass
        
        
    #AI METHOD HERE
    def chooseCard(self):
        return self.hand[0]
                
class History(object):
    def __init__(self):
        self.moves = []

    def recordMove(self, player, card, result):
        self.moves.append((player, card, result))


    
    
    
    
    
#
