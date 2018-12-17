from infrastructure import *

class Feature(object):
    def __init__ (self, fstate, action, combostate):
        self.fstate = fstate
        self.action = action
        self.combostate = combostate

    def f(fstate, action, combostate):
        pass

class SizeofHand(Feature):
    def __init__ (self, fstate, action, combostate):
        self.fstate = fstate
        self.action = action
        self.combostate = combostate

    def f(self):
        cards = 0
        for x in self.fstate.hand:
            cards += 1
        return cards

# Cards over 10
class HighCount(Feature):
    def __init__ (self, fstate, action, combostate):
        self.fstate = fstate
        self.action = action
        self.combostate = combostate
    def f(self):
        highCards = 0
        for card in self.fstate.hand:
            if card.value >= 10:
                highCards += 1 
        return highCards
            
# Cards under 6
class LowCount(Feature):
    def __init__ (self, fstate, action, combostate):
        self.fstate = fstate
        self.action = action
        self.combostate = combostate
    def f(self):
        lowCards = 0
        for card in self.fstate.hand:
            if card.value <= 6:
                lowCards += 1 
        return lowCards

# Cards under 6
class LowCount(Feature):
    def __init__ (self, fstate, action, combostate):
        self.fstate = fstate
        self.action = action
        self.combostate = combostate
    def f(self):
        medCards = 0
        for card in self.fstate.hand:
            if card.value > 6:
                if card.value < 10:
                    medCards += 1 
        return medCards

# checker if it works with rule state
# check against last card and make sure it works=
class Illegality(Feature):
    def __init__ (self, fstate, action, combostate):
        self.checker = Checker()
        self.fstate = fstate
        self.action = action
        self.combostate = combostate

    def f(self):
        actionCard = self.action
        lastCard = self.fstate.lastCard
        constraintState = combostate.state
        isLegalGivenState = self.checker.isConsistent(Notification(LEGAL, actionCard, lastCard), constraintState)
        if isLegalGivenState:
            return 1
        else:
            return 0

class WildValue(Feature):
    def __init__ (self, fstate, action, combostate):
        self.fstate = fstate
        self.action = action
        self.combostate = combostate

    def f(self):
        wildvals = 0
        for card in self.fstate.hand:
            if card.value == self.combostate.state.wildValueRule.setting:
                wildvals += 1 
        return wildvals

class MajorityPercent(Feature):
    def __init__ (self, fstate, action, combostate):
        self.fstate = fstate
        self.action = action
        self.combostate = combostate

    def f(self):
        c = 0
        s = 0
        h = 0
        d = 0
        maxsuit = 0 
        for card in self.fstate.hand:
            if card.suit == "C":
                c += 1 
            if card.suit == "D":
                d += 1 
            if card.suit == "S":
                s += 1 
            if card.suit == "H":
                h += 1 
        maxsuit = max([c,s,h,d])
        return (maxsuit/float(len(self.fstate.hand)))

def featureDict(feature, state, action, combo ):
    featureDict = {}
    for feature in featureList:
        featureDict[feature] = feature(state,action,combo).f()
    return featureDict

def R(fstate, action, combo, nextFstate):
    if len(fstate.hand) - len(nextFstate.hand) == 1:
        
        if len(nextFstate.hand) == 0:
            # you won!
            return 500
        else:
            return 1
    if len(fstate.hand) - len(nextFstate.hand) == -1:
        return -1
    if len(fstate.hand) - len(nextFstate.hand) == -2:
        return -2
    if len(fstate.hand) == len(nextFstate.hand):
        return 0
    else:
        return 0

    
# \\\\\\\\\\\\\\\\
# 
# Testing stuff
# 
# ////////////////

# Fake rules gethhelelp
bvRule = Rule('basicValueRule', 2)
wvRule = Rule('wildValueRule', 13)
wsRule = Rule('wildSuitRule', 'C')
pdRule = Rule('poisonDistRule', 9)

# fake effects (not inited)
pcRule = Rule('poisonCardRule', 99)
soRule = Rule('screwOpponentRule', 99)
spRule = Rule('skipPlayerRule', 99)

# fake state
ruleState = State(bvRule, wvRule, wsRule, pdRule)
effectState = EffectState(pcRule, soRule,spRule)

# combined
combostate = CombinedState(ruleState,effectState)

# Cards
card1 = Card(2, "C")
card2 = Card(13, "H")
card3 = Card(14, "S")

testFstate = Fstate([card1, card3], card2)
testAction = card2

# print Illegality(testFstate, testAction, combostate).f()

print featureDict([Illegality, LowCount], testFstate, testAction, combostate)