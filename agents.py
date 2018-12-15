from player import *
import random
import sys

trueState = State(Rule(BASICVALUE, True), Rule(BASICSUIT, "S"), Rule(WILDVALUE, None), Rule(WILDSUIT, None))

class Agent(Player):
    def __init__(self, name):
        super(Player, self).__init__(name)    
    
    # return the card from your hand you want to play
    def chooseCard(self, lastCard):
        pass #DO NOT CHANGE
    
    # notified of an event in the game (a penalty, a success, or a win)
    def notify(self, notification, game):
        pass #DO NOT CHANGE
    
    # change a rule via the makeModification function, which takes a "rule" tuple as its only argument
    def modifyRule(self, makeModification):
        pass #DO NOT CHANGE
        
    # # choose an opponent index and a card to give an opponent
    # # Note: don't remove the card. Just return it. The game will remove it
    # # return a (targetIndex, unwantedCard) tuple.
    # def screwOpponent(self, otherPlayers):
    #     pass # let's players give another player one of their cards
    
    # put here to avoid copy-paste into all agents. NOTE: Change eventually.
    def screwOpponent(self, playerList):
        targets = []
        for i, player in enumerate(playerList):
            if player.name != self.name:
                targets.append(player)
        if (targets.empty()):
            print "this really shouldn't happen -- in screw opponent"
            return (0, random.choice(self.hand)) #error checking
        else:
            return (random.choice(targets), random.choice(self.hand))

    # this is how you know if the move you just made is legal or not
    def getFeedback(self, isLegal):
        pass # DO NOT CHANGE

class RandomAgent(Agent):
    def __init__(self, name):
        super(Agent, self).__init__(name)
        
        self.wins = 0
        self.roundLegals = 0
        self.roundIllegals = 0
        self.validPercentByRound = []
        
    def screwOpponent(self, playerList):
        targets = []
        for i, player in enumerate(playerList):
            if player.name != self.name:
                targets.append(player)
        if (targets.empty()):
            print "this really shouldn't happen -- in screw opponent"
            return (0, random.choice(self.hand)) #error checking
        else:
            return (random.choice(targets), random.choice(self.hand))
                
    
    def notify(self, notification, game):
        def newRound():
            if self.roundIllegals + self.roundLegals == 0: return #don't divide by 0
            self.validPercentByRound.append(float(self.roundLegals) / (self.roundIllegals + self.roundLegals) )
            self.roundLegals = 0
            self.roundIllegals = 0
            
        if notification.type == WON: #corresponds to "won"
            newRound()
        
    
    def modifyRule(self, makeModification):
        ruletype = random.choice([BASICVALUE, WILDVALUE, WILDSUIT])
        #
        if ruletype == BASICVALUE:
            newGreater = random.choice([True, False])
            rule = Rule(BASICVALUE, newGreater)
            
            makeModification(rule)
            
        elif ruletype == WILDVALUE:
            lst = [i + 2 for i in range(13)]
            lst.append(None)
            newValue = random.choice(lst)
            rule = Rule(WILDVALUE, newValue)
            
            makeModification(rule)
        
        elif ruletype == WILDSUIT:
            newSuit = random.choice(["D", "H", "S", "C", None])
            rule = Rule(WILDSUIT, newSuit)
            
            makeModification(rule)
    
    def chooseCard(self, lastCard):
        return self.hand[0]
        # return random.choice([self.hand])
    
    def getFeedback(self, isLegal):
        if isLegal:
            self.roundLegals += 1
        else:
            self.roundIllegals += 1

    

class HumanAgent(Agent):
    def __init__(self, name):
        super(Agent, self).__init__(name)
    
    def chooseCard(self, lastCard, aggressive=False):
        def showHand():
            for index, card in enumerate(self.hand):
                print "Index:", index, " -- ", card
        while True:
            # show your hand
            if not aggressive:
                print "the LAST CARD that was played was:", lastCard
            print "your hand is: \n"
            showHand()
            if aggressive:
                print "\nWhich card are you tryna stick your opponent with?"
            else:
                print "\ntype the index of the card you want to play: "
            
            instr = raw_input()
            if instr == "q":
                print "quitting"
                sys.exit()
            try:
                index = int(instr)
                return self.hand[index]
            except:
                print "\n\n**INVALID SELECTION** Try again: \n\n"
        
    def screwOpponent(self, playerList):
        print "choose the opponent you want to screw over (by typing their index)"
        for i, player in enumerate(playerList):
            print "Index:", i, " -- ", player.name, "Tot cards: ", len(player.hand)
        targetIndex = input()
        unwantedCard = self.chooseCard(None, True)
        return (targetIndex, unwantedCard)
        
    def modifyRule(self, makeModification):
        def getActiveValue():
            print "type the value (from 2 to 14) you want to activate, or 0 to inactivate"
            value = int(input())
            if (value >= 2 and value <= 14):
                return value
            elif value == 0:
                return None
            else:
                print "invalid -- try again"
        try:
            print "congrats, you get to change a rule! Please be precise"
            print "type the rule you want to change:"
            print "  1 for basicValue\n  3 for WildValue\n  4 for WildSuit \n  5 for PoisonDist"
            print "  6 for PoisonCard\n  7 for ScrewOpponent\n  8 for SkipPlayer"
            rule = int(input())
            
            if rule == BASICVALUE:
                print "type 0 to make lower cards have priority, and 1 to make higher cards have priority"
                newGreater = int(input())
                newGreater = False if newGreater == 0 else True
                
                ruleTuple = Rule(BASICVALUE, newGreater)
                makeModification(ruleTuple)
                
                return
                
            elif rule == WILDVALUE:
                # print "type in a value between 2 and 14 to make that the new wild value"
                # newValue = int(input())
                newValue = getActiveValue()
                
                ruleTuple = Rule(rule, newValue)
                makeModification(ruleTuple)
                
                return
                
            elif rule == WILDSUIT:
                while True:
                    print "type in S, D, C, or H to change your suit"
                    suit = raw_input().upper()
                    if len(suit) == 1 and suit in "SDCH":
                        
                        ruleTuple = Rule(WILDVALUE, suit)
                        makeModification(ruleTuple)
                        
                        return
                    else:
                        print "invalid character, try again"
                        
            elif rule == POISONDIST:
                print "type 1 or 2 to make either 1 or 2 distance poisonous, and 0 to inactivate"
                result = input()
                if result == 0:
                    value = None
                elif result == 1 or result == 2:
                    value = result
                else:
                    print "invalid selection"
                    return
                makeModification((Rule(POISONDIST, value)))
                return
            
            elif rule == POISONCARD or rule == SKIPPLAYER or rule == SCREWOPPONENT:
                value = getActiveValue() #returns a value between 2-14 or None
                makeModification(Rule(rule, value))
                return
        except:
            print "invalid input -- continuing unchanged"
            return
        
    def notify(self, notification, game):
        pass

class LearningAgent(Agent):
    def __init__(self, name):
        super(Agent, self).__init__(name)
        self.wins = 0
        self.roundLegals = 0
        self.roundIllegals = 0
        self.validPercentByRound = []    
        
        self.beliefs = Counter()
        
        for state in stateList:
            self.beliefs[state] = 0

    # return the card from your hand you want to play
    def chooseCard(self, lastCard):
        belief_state = self.beliefs.argMax() 
        legal_cards = []
        c = Checker()
        for index, card in enumerate(self.hand):
            notification = Notification(LEGAL, card, lastCard)
            if c.isConsistent(notification, belief_state):
                legal_cards.append(card)

        if len(legal_cards) != 0:
            return random.choice(legal_cards)
        else: 
            return random.choice(self.hand)
    
    # notified of an event in the game (a penalty, a success, or a win)
    def notify(self, notification, game):
    # n = Notification(LEGAL, Card(4, "H"), Card(7, "D"))
        def newRound():
            if self.roundIllegals + self.roundLegals == 0: return #don't divide by 0
            self.validPercentByRound.append(float(self.roundLegals) / (self.roundIllegals + self.roundLegals) )
            self.roundLegals = 0
            self.roundIllegals = 0
        if notification.type == LEGAL:
            res = True
        elif notification.type == PENALTY:
            res = False
        elif notification.type == WON: #corresponds to "won"
            newRound()
            return

        states_agree = []
        c = Checker()
        for state in stateList:
            if c.isConsistent(notification, state) == res:
                states_agree.append(state)

        for state in stateList:
            if state in states_agree:
                self.beliefs[state] += 1.0 / len(states_agree)
            else:
                self.beliefs[state] = 0

        self.beliefs.normalize()

    
    # change a rule via the makeModification function, which takes a "rule" tuple as its only argument
    def modifyRule(self, makeModification):
        ruletype = random.choice([BASICVALUE, WILDVALUE, WILDSUIT])
        #
        if ruletype == BASICVALUE:
            newGreater = random.choice([True, False])
            rule = Rule(BASICVALUE, newGreater)
            
            makeModification(rule)
            
        elif ruletype == WILDVALUE:
            lst = [i + 2 for i in range(13)]
            lst.append(None)
            newValue = random.choice(lst)
            rule = Rule(WILDVALUE, newValue)
            
            makeModification(rule)
        
        elif ruletype == WILDSUIT:
            newSuit = random.choice(["D", "H", "S", "C"])
            rule = Rule(WILDSUIT, newSuit)
            
            makeModification(rule)

    # this is how you know if the move you just made is legal or not
    def getFeedback(self, isLegal):
        if isLegal:
            self.roundLegals += 1
        else:
            self.roundIllegals += 1
        
class HmmAgent(Agent):
    def __init__(self, name):
        super(Agent, self).__init__(name)
        self.checker = Checker()
        self.beliefDistrib = Counter()
        
        self.roundIllegals = 0
        self.roundLegals = 0
        self.validPercentByRound = []
        
        # initialize list of states
        initProb = 1 / float(len(stateList))
        for s in stateList:
            self.beliefDistrib[s] = initProb
    
    # return the card from your hand you want to play
    def chooseCard(self, lastCard):
        belief_state = self.beliefDistrib.argMax() 
        legal_cards = []
        for index, card in enumerate(self.hand):
            notification = Notification(LEGAL, card, lastCard)
            if self.checker.isConsistent(notification, belief_state):
                legal_cards.append(card)

        if len(legal_cards) != 0:
            return random.choice(legal_cards)
        else: 
            return random.choice(self.hand)
            
    def getFeedback(self, isLegal):
        if isLegal:
            self.roundLegals += 1
        else:
            self.roundIllegals += 1
    
    # notified of an event in the game (a penalty, a success, or a win)
    def notify(self, notification, game):
        
        if notification.type == WON:
            # simulate dynamics -- occurs only on new round change
            #naive dynamics: reset the list
            uniformProb = 1.0 / float(len(stateList))
            for state in stateList:
                self.beliefDistrib[state] = uniformProb # naive
            self.validPercentByRound.append(float(self.roundLegals) / (self.roundIllegals + self.roundLegals) )
            self.roundLegals = 0
            self.roundIllegals = 0
            return
            
            #complex dynamics:
            # for each state with non-zero probability
              # find successor states, and add them as possiblities. But weight towards current state
              # then, renormalize the entire thing
            
        else:
            if notification.type == LEGAL:
                res = True
            elif notification.type == PENALTY:
                res = False
            # update probabilities based on state dynamics
            for state in stateList: #same thing as belief distribution
                if self.beliefDistrib[state] == 0:
                    continue
                else:
                    if self.checker.isConsistent(notification, state) == res:
                        continue
                    else:
                        self.beliefDistrib[state] = 0
            return
