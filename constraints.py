#abstract class for a constraint
class Constraint(object):
    # returns a bool. True if the constraint should be activated
    # ex) maybe every time two cards of the same type are placed, the next player is skipped
    def isActive(self, attemptedCard):
        pass
    
    def isLegal(self, attemptedCard, lastCard):
        pass


class BasicValueConstraint(Constraint):
    """
    Tells you if higher or lower cards can be played, init with bool greater
      in general, if card is equal or (greater/less), then it is legal
    """
    def __init__(self, greater): #greater is a boolean to say if greater values are allowed, or lower values are
        self.greater = greater

    # never conditionally active
    def isActive(self, attemptedCard):
        return True
    
    def isLegal(self, attemptedCard, lastCard):
        if self.greater:
            return attemptedCard.value >= lastCard.value
        else:
            return attemptedCard.value <= lastCard.value
    
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
    
    def isActive(self, attemptedCard):
        return True
    
    def isLegal(self, attemptedCard, lastCard):
        return attemptedCard.suit == lastCard.suit
        
class WildValueEffect(Constraint):
    """
    Allows for a "wild value"
    """
    def __init__(self):
        self.wildValue = None #basic game rule
    
    def isActive(self, attemptedCard):
        return self.wildValue != None
    
    def isLegal(self, attemptedCard, lastCard):
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
    def __init__(self):
        self.wildSuit = None
    
    def isActive(self, attemptedCard):
        return self.wildSuit != None
    
    def isLegal(self, attemptedCard, lastCard):
        return attemptedCard.suit == self.wildSuit
    
    def modify(self, suit):
        """
        Give it a suit or None to change the value of this constraint
        """
        self.wildSuit = suit
        
