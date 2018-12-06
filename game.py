from infrastructure import *
from collections import namedtuple
import copy

Notification = namedtuple('Notification', ['type', 'card'])

#notification types
LEGAL = 1
PENALTY = 2
WON = 3

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



class Game(object):
    def __init__(self, players):
        
        # constraints
        self.basicValueConstraint = BasicValueConstraint(True, self)
        self.basicSuitConstraint = BasicSuitConstraint(self)
        self.wildValueEffect = WildValueEffect(self)
        self.wildSuitEffect = WildSuitEffect(self)
        
        # player stuff
        self.players = players
        self.activePlayer = 0 # the player after the dealer goes first. keeps track of which player is up
        
        #deck stuff
        self.startingHandSize = 5
        self.changeRuleRate = 1
        self.deck = Deck() #pre-shuffled deck
        self.pile = [] # a list of discarded cards. DIFFERENT FROM DECK OBJECT. 
        self.lastCard = None
        
        self.round = 0 # record which round we are on
        self.gameHistory = GameHistory() # records the history of the game for training data
        self.roundHistory = RoundHistory()
        
    def isLegal(self, attemptedCard):
        """ 
        Evaluates the card against the current constraints to see whether it is viable or not
        Returns True or False
        """
        #try effects. needs only ONE to return True
        wildEffects = [self.wildValueEffect, self.wildSuitEffect]
        
        for effect in wildEffects:
            if (effect.isActive(attemptedCard)):
                if (effect.isLegal(attemptedCard)):
                    return True
        
        # try the basics (ie, ordering and other). These are always active
        # need only ONE to pass as true
        basicConstraints = [self.basicValueConstraint, self.basicSuitConstraint]
        
        for constraint in basicConstraints:
            if (constraint.isLegal(attemptedCard)):
                return True
        return False # if all the constraints pass, return true
        
    
    def notifyAll(self, notification):
        """
        Notifies all players of a change in the gamestate.
        The "game history" is also notified
        """
        # print stuff for human players for human players
        type = notification.type
        
        print self.players[self.activePlayer].name
        if type == LEGAL:
            # self.roundHistory.recordMove(notification)
            print "LEGAL CARD PLAYED:", notification.card, "\n"
        elif type == PENALTY:
            # self.roundHistory.recordMove(notification)
            print "ILLEGAL CARD PLAYED:", notification.card, "\n"
        elif type == WON:
            print "Player", self.players[self.activePlayer].name, "won!"
        
        for player in self.players:
            player.notify(notification, self)
            
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
                # NOTE: THESE ARE UNTESTED!!! WATCH OUT FOR THIS SECTION!
                # make a new deck using the pile
                origLen = len(self.pile) # for assert
                self.deck.cards = copy.copy(self.pile) #preserves references I think
                self.pile = []
                assert( origLen == len(self.deck.cards) ) #copying trips me out
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
        
        Returns the player number of the winner of the round.
        """
        def initNewRound(prevWinner): # resets the deck and pile after the end of each round
            self.activePlayer = prevWinner
            self.deck = Deck() #maybe not the best, but we can optimize later. ideally we fetch cards from every player
            self.pile = []
            self.roundHistory = RoundHistory() # declare a new round
            
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
                
        # closing the round off
        self.gameHistory.addRound(self.roundHistory)
        self.round += 1
        
        # modify the rules every fifth round
        if (self.round % self.changeRuleRate == 0):
            self.players[self.activePlayer].modifyRule(self)
        
        return self.activePlayer
        
    
    def playGame(self, numRounds=10):
        winner = 0
        for i in range(numRounds):
            winner = self.playRound(winner)
            
    

            


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
        
class WildSuitEffect(Constraint):
    """
    Allows for a "Wild Suit" -- this suit trumps all other suits
    """
    def __init__(self, game):
        self.game = game
        self.wildSuit = None
    
    def isActive(self, attemptedCard):
        return self.wildSuit != None
    
    def isLegal(self, attemptedCard):
        return attemptedCard.suit == self.wildSuit
    
    def modify(self, suit):
        """
        Give it a suit or None to change the value of this constraint
        """
        self.wildSuit = suit
        

# tests
pHuman = Player("J", True)
pBot = Player("Bot")

g = Game([pHuman, pBot])

g.playGame()





#
