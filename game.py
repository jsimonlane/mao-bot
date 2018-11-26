from infrastructure import *

class Game(object):
    def __init__(self, players):
        self.AndConstraints = [] #this constraint must pass. ex) player order 
        self.OrConstraints = [] # only one of these constraints needs to pass. ex) higher value, or same suit can be played
        self.players = players
        self.activePlayer = 0 # the player after the dealer goes first. keeps track of which player is up
        self.deck = Deck() #pre-shuffled deck

        self.pile = [] # shows the cards that have been accepted
        self.lastCard = None
        self.round = 0 # record which round we are on
        self.history = History() # records the history of the game for training data
        
    # allows for communication between the game and the players
    def notifyAll(action):
        for player in players:
            player.notify(action)
            
    def drawCard(self):
        draw = self.deck.drawCard()
        if draw:
            return draw
        else: 
            self.deck.cards = self.pile
            self.deck.shuffle()
    
    def newRound(self, prevWinner): # resets the deck and pile after the end of each round
        self.activePlayer = prevWinner
        self.deck = Deck()
        self.pile = []
        self.lastCard = None


#abstract class for a constraint
class Constraint(object):
    # returns a bool. True if the constraint should be activated
    # ex) maybe every time two cards of the same type are placed, the next player is skipped
    def isActive(self, card):
        pass
    
    def isLegal(self, card):
        pass

# tells you if higher or lower cards can be played, init with bool greater
# in general, if card is equal or (greater/less), then it is legal
class CardOrder(Constraint):
    def __init__(self, greater): #greater is a boolean to say if greater values are allowed, or lower values are
        self.greater = greater
        self.prevCard
    
    # never conditionally active
    def isActive(self, card):
        return True
        
    # updates the last card that was played
    def setPrevCard(self, card):
        self.prevCard = card
    
    def isLegal(self, card):
        if self.greater:
            return card.value >= prevCard.value
        else:
            return card.value <= prevCard.value
        
        








#
