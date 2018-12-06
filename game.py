from infrastructure import *
import constraints

import copy
from player import *


class Game(object):
    def __init__(self, players, autogame = False):
        
        # constraints
        self.basicValueConstraint = constraints.BasicValueConstraint(True, self)
        self.basicSuitConstraint = constraints.BasicSuitConstraint(self)
        self.wildValueEffect = constraints.WildValueEffect(self)
        self.wildSuitEffect = constraints.WildSuitEffect(self)
        
        # player stuff
        self.players = players
        self.activePlayer = 0 # the player after the dealer goes first. keeps track of which player is up
        self.autogame = autogame
        
        #deck stuff
        self.startingHandSize = 5
        self.changeRuleRate = 1
        self.deck = Deck() #pre-shuffled deck
        self.pile = [] # a list of discarded cards. DIFFERENT FROM DECK OBJECT. 
        self.lastCard = None
        
        #round stuff
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
        
        if not self.autogame: print self.players[self.activePlayer].name
        if type == LEGAL:
            # self.roundHistory.recordMove(notification)
            if not self.autogame: print "LEGAL CARD PLAYED:", notification.card, "\n"
        elif type == PENALTY:
            # self.roundHistory.recordMove(notification)
            if not self.autogame: print "ILLEGAL CARD PLAYED:", notification.card, "\n"
        elif type == WON:
            if not self.autogame: print "Player", self.players[self.activePlayer].name, "won!"
        
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
            
            #tell player of legality
            player.wellPlayed()
            
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
                
            #tell player of illegality
            player.badlyPlayed()
                
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
            # print "It is the turn of: ", self.players[self.activePlayer].name
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
            

# tests
pHuman = Player("J")
pBot = Player("Bot")

g = Game([pHuman, pBot], True)

g.playGame(1000)

#print stats
for player in g.players:
    print player.name
    print player.wins
    print player.validPercentByRound[0]





#
