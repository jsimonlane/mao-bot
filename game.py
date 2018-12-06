from infrastructure import *
from collections import namedtuple
import copy

Notification = namedtuple('Notification', ['type', 'card'])

#notification types
LEGAL = 1
PENALTY = 2
WON = 3



class Game(object):
    def __init__(self, players):
        
        # constraint stuff
        self.baseConstraints = [BasicValueConstraint(True, self), BasicSuitConstraint(self)] # list containing basic constraints
        self.wildEffects = [WildValueEffect(self), TrumpSuitEffect(self)] # list containing the two wild cards
        
        # player stuff
        self.players = players
        self.activePlayer = 0 # the player after the dealer goes first. keeps track of which player is up
        
        #deck stuff
        self.startingHandSize = 5
        self.deck = Deck() #pre-shuffled deck
        self.pile = [] # a list of discarded cards. DIFFERENT FROM DECK OBJECT. 
        self.lastCard = None
        
        self.round = 0 # record which round we are on
        self.history = History() # records the history of the game for training data
        
    def isLegal(self, attemptedCard):
        """ 
        Evaluates the card against the current constraints to see whether it is viable or not
        Returns True or False
        """
        #try effects. needs only ONE to return True
        for effect in self.wildEffects:
            if (effect.isActive(attemptedCard)):
                if (effect.isLegal(attemptedCard)):
                    return True
        
        # try the basics (ie, ordering and other). These are always active
        # need only ONE to pass as true
        for constraint in self.baseConstraints:
            if (constraint.isLegal(attemptedCard)):
                return True
        return False # if all the constraints pass, return true
        
    # allows for communication between the game and the players
    def notifyAll(self, notification):
        # print stuff for human players for human players
        type = notification.type
        
        print self.players[self.activePlayer].name
        if type == LEGAL:
            print "LEGAL CARD PLAYED:", notification.card, "\n"
        elif type == PENALTY:
            print "ILLEGAL CARD PLAYED:", notification.card, "\n"
        elif type == WON:
            print "Player", self.players[self.activePlayer].name, "won!"

        
        
        for player in self.players:
            player.notify(notification)
            
    # gets a card from the deck. Resets the pile if necessary.
    # returns None if all the cards are in players hands (god help us)
    def getCardFromDeck(self):
        card = self.deck.drawCard()
        # for durability, reset the deck
        if (card == None):
            assert (len(self.deck.cards) == 0)
            if (len(self.pile) == 0):
                #sheesh. literally all the cards have been played
                return None
            else:
                # make a new deck using the pile
                origLen = len(self.pile) # for assert
                self.deck.cards = copy.copy(self.pile) #preserves references I think
                self.pile = []
                assert (origLen == len(self.deck.cards)) #copying trips me out
                self.deck.shuffle()
                return self.getCardFromDeck() #recurse, try to get another card
        else:
            return card
    
    # describes what happens during a player turn
    #    
    # returns WON if a player won, 0 if not
    def playerTurn(self, player):
        """
        Describes and handles logic for a player attempting to place a card
        
        Returns WON if the player won, and 0 if not
        """
        attemptedCard = player.takeAction(self.lastCard) # the player tries to play a card
        feedback = self.isLegal(attemptedCard) # the card is evaluated for legality
        
        if feedback == LEGAL:
            # game state bookkeeping -- last card, and the pile
            self.pile.append(attemptedCard)
            self.lastCard = attemptedCard
            
            # notify all players of legality
            notification = Notification(LEGAL, attemptedCard)
            self.notifyAll(notification)
            
            #handle win conditions
            if player.won():
                return WON
            else:
                return 0
        else:
            # return the card to the player, and penalize them with a new card
            player.takeCard(attemptedCard)
            penaltyCard = self.getCardFromDeck()
            if penaltyCard:
                player.takeCard(penaltyCard)
                
            # notify all players of the penalty
            notification = Notification(PENALTY, attemptedCard)
            self.notifyAll(notification) 
        
    def playRound(self, prevWinner=0):
        """
        Plays a single round of the Mao card game. 
        Initilalized with whoever the previous winner was
        
        Returns Void
        """
        def initNewRound(prevWinner): # resets the deck and pile after the end of each round
            self.activePlayer = prevWinner
            self.deck = Deck() #maybe not the best, but we can optimize later
            self.pile = []
            
            # initialize the first card that is placed
            initialCard = self.getCardFromDeck()
            self.pile.append(initialCard)
            self.lastCard = initialCard
            
            for player in self.players:
                # draw 5 cards
                player.hand = [self.getCardFromDeck() for i in range(self.startingHandSize)]
                
                
        initNewRound(prevWinner)
        
        while True:
            print "It is the turn of: ", self.players[self.activePlayer].name
            player = self.players[self.activePlayer]
            result = self.playerTurn(player)
            if result == WON:
                notification = Notification(WON, None)
                self.notifyAll(notification)
                break
            else:
                self.activePlayer = (1 + self.activePlayer) % len(self.players)
                
        
        # include some change rule stuff here!
            
    

            


#abstract class for a constraint
class Constraint(object):
    # returns a bool. True if the constraint should be activated
    # ex) maybe every time two cards of the same type are placed, the next player is skipped
    def isActive(self, card):
        pass
    
    def isLegal(self, card):
        pass


class BasicValueConstraint(Constraint):
    """
    Tells you if higher or lower cards can be played, init with bool greater
      in general, if card is equal or (greater/less), then it is legal
    """
    def __init__(self, greater, game): #greater is a boolean to say if greater values are allowed, or lower values are
        self.greater = greater
        self.game = game # way to refer back to the parent game

    # never conditionally active
    def isActive(self, attemptedCard):
        return True
    
    def isLegal(self, attemptedCard):
        if self.greater:
            return attemptedCard.value >= self.game.lastCard.value
        else:
            return attemptedCard.value <= self.game.lastCard.value
    
    def modify(self, greaterBool):
        """
        if greaterBool is true, greater cards now win.
        if greaterBool is false, lower cards now win.
        """
        self.greater = greaterBool
            
class BasicSuitConstraint(Constraint):
    """
    The basic constraint that says cards may be of the same suit 
      as the lastCard (card on top of the deck)
    """
    def __init__(self, game):
        self.game = game
    
    def isActive(self, attemptedCard):
        return True
    
    def isLegal(self, card):
        return card.suit == self.game.lastCard.suit
        
class WildValueEffect(Constraint):
    """
    Allows for a "wild value"
    """
    def __init__(self, game):
        self.game = game
        self.wildValue = 7 #basic game rule
    
    def isActive(self, attemptedCard):
        return self.wildValue != None
    
    def isLegal(self, attemptedCard):
        return attemptedCard.value == self.wildValue
    
    def modify(self, value):
        """
        Give it an int between [2,15] or None to change the rank of this constraint
        """
        self.wildValue = value
        
class TrumpSuitEffect(Constraint):
    """
    Allows for a "Trump Suit Suit"
    """
    def __init__(self, game):
        self.game = game
        self.trumpSuit = None
    
    def isActive(self, attemptedCard):
        return self.trumpSuit != None
    
    def isLegal(self, attemptedCard):
        return attemptedCard.suit == self.trumpSuit
    
    def modify(self, suit):
        """
        Give it a suit or None to change the value of this constraint
        """
        self.trumpSuit = suit
        

# tests
pHuman = Player("J", True)
pBot = Player("Bot")

g = Game([pHuman, pBot])

g.playRound()





#
