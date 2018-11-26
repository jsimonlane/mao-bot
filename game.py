from infrastructure import *

#notifications
LEGAL = 1
PENALTY = 2



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
    def notifyAll(self, notification):
        for player in players:
            player.notify(notification)
            
    # gets a card from the deck. Returns None if no cards are left
    def getCardFromDeck(self):
        card = self.deck.drawCard()
        # for durability, reset the deck
        if (card == None):
            #make a new round
        else:
            return card
    
    #         
    # returns 1 if a player won, 0 if not
    def playerTurn(self, player):
        attemptedCard = player.takeAction()
        feedback = self.isLegal(attemptedCard)
        if feedback == LEGAL:
            notification = (LEGAL, attemptedCard)
            notifyAll(notification)
            if player.won():
                return 1
            else:
                return 0
        else:
            # return the card to the player, and penalize them with a new card
            player.takeCard(attemptedCard)
            penaltyCard = self.getCardFromDeck()
            if penaltyCard:
                player.takeCard(penaltyCard)
            notification = (PENALTY, attemptedCard) #add self.cardBefore?
            notifyAll(notification) 
        
    def playRound(self):
        while True:
            player = self.players[self.activePlayer]
            result = self.playerTurn(player)
            if result == 0:
                break
            else:
                activePlayer = (1 + self.activePlayer) % len(self.players)
        # include some change rule stuff here!
            
<<<<<<< HEAD
    def drawCard(self):
        draw = self.deck.drawCard()
        if draw:
            return draw
        else: 
            self.deck.cards = self.pile
            self.deck.shuffle()
=======
            
        
>>>>>>> GameInfraUpdates
    
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
