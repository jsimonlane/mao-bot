# these are different from constraints in that the card is always allowed --
#  however, it lets the player modify some other aspect of the game in some way

from infrastructure import *

class Effect(object):
    def isActive(self, attemptedCard):
        """
        Returns a Boolean.
        Determines whether the effect should be activated or not.
        Generally, checks to see whether the effect is on, AND that the attempted 
        card matches the current rule criteria
        """
        pass
        
    def enactEffect(self, game):
        """
        Modifies the state of the game. Ensure to include a "notify all"
        """
        pass
        
    def modify(self):
        """
        Arguments vary. Modifies the state of the effect
        """
    
class ScrewOpponentEffect(Effect):
    def __init__(self):
        self.activatingValue = None #should be a value in [2,14], or None
        
    def isActive(self, attemptedCard):
        return attemptedCard.value == self.activatingValue
        
    def enactEffect(self, game):
        # if the player has a card to give, let them give a card
        # i think this is all done by reference, so we should be ok
        activePlayer = game.players[game.activePlayer]
        
        if (len(activePlayer.hand) > 0):
            (targetIndex, unwantedCard) = activePlayer.screwOpponent(game.players)
            activePlayer.hand.remove(unwantedCard)
            game.players[targetIndex].hand.append(unwantedCard)
    
        notification = Notification() #make notification here. TODO
        game.notifyAll()
        
    
    def modify(self, newActivatingValue):
        if newActivatingValue == None or (newActivatingValue >= 2 and newActivatingValue <= 14):
            self.activatingValue = self.newActivatingValue
        else:
            print "invalid activating value for ScrewOpponent"


# SERIOUSLY SKETCHED OUT BY activePlayer INCREMENTING -- implement last
class SkipPlayerEffect(Effect):
    def __init__(self):
        self.activatingValue = None #should be a value in [2,14], or None
        
    def isActive(self, attemptedCard):
        return attemptedCard.value == self.activatingValue
        
    def enactEffect(self, game):
        # this really concerns me -- WATCH OUT
        game.activePlayer = (game.activePlayer + 1) % len(game.players)
        
        notification = Notification() #make notification here. TODO
        game.notifyAll()
    
    def modify(self, newActivatingValue):
        if newActivatingValue == None or (newActivatingValue >= 2 and newActivatingValue <= 14):
            self.activatingValue = self.newActivatingValue
        else:
            print "invalid activating value for SkipPlayer"





#
