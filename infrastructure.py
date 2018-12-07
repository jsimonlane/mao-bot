import random
from collections import namedtuple

import constraints

Card = namedtuple('Card', ['value', 'suit'])

# rule settings
Rule = namedtuple('Rule', ['rule', 'setting'])
BASICVALUE = 1
BASICSUIT = 2 # I don't think there's much we can do with this as of now
WILDVALUE = 3
WILDSUIT = 4


State = namedtuple('State', ['basicValueRule', 'basicSuitRule', 'wildValueRule', 'wildSuitRule'])

# checker.isConsistent(notification, ruleState)
  # returns True if lastCard, attemptedCard is consistent with the given rule state


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




#copy and paste
class Checker(object):
    def __init__(self):
        self.basicValueConstraint = constraints.BasicValueConstraint(True)
        self.basicSuitConstraint = constraints.BasicSuitConstraint()
        self.wildValueEffect = constraints.WildValueEffect()
        self.wildSuitEffect = constraints.WildSuitEffect()
        self.lastCard = None

    def makeModification(self, ruleTuple):
        rule = ruleTuple.rule
        setting = ruleTuple.setting

        if rule == BASICVALUE:
            self.basicValueConstraint.modify(setting)
        elif rule == BASICSUIT:
            pass
        elif rule == WILDSUIT:
            self.wildSuitEffect.modify(setting)
        elif rule == WILDVALUE:
            self.wildValueEffect.modify(setting)

    def isLegal(self, attemptedCard):
        """ 
        Evaluates the card against the current constraints to see whether it is viable or not
        Returns True or False
        """
        #try effects. needs only ONE to return True
        wildEffects = [self.wildValueEffect, self.wildSuitEffect]

        for effect in wildEffects:
            if (effect.isActive(attemptedCard)):
                if (effect.isLegal(attemptedCard, self.lastCard)):
                    return True

        # try the basics (ie, ordering and other). These are always active
        # need only ONE to pass as true
        basicConstraints = [self.basicValueConstraint, self.basicSuitConstraint]

        for constraint in basicConstraints:
            if (constraint.isLegal(attemptedCard, self.lastCard)):
                return True
        return False # if all the constraints pass, return true

    def isConsistent(self, notification, ruleState):
        # change the state
        self.lastCard = notification.lastCard
        for rule in ruleState:
            self.makeModification(rule)
        # see if is legal
        return self.isLegal(notification.attemptedCard)
    

# checker tests
# n = Notification(LEGAL, Card(4, "H"), Card(7, "D"))
# s = State(Rule(BASICVALUE, True), Rule(BASICSUIT, None), Rule(WILDVALUE, 5), Rule(WILDSUIT, "H") )
# 
# c = Checker()
# 
# print c.isConsistent(n, s)
#
