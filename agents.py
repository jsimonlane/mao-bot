from player import *
import random
import sys

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
    
    def chooseCard(self, lastCard):
        def showHand():
            for index, card in enumerate(self.hand):
                print "Index:", index, " -- ", card
        while True:
            # show your hand
            print "the LAST CARD that was played was:", lastCard
            print "your hand is: \n"
            showHand()
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
        
        
    def modifyRule(self, makeModification):
        while True:
            print "congrats, you get to change a rule! Please be precise"
            print "type the rule you want to change -- 1 for basicValue, 3 for WildValue, and 4 for WildSuit"
            rule = int(input())
            
            if rule == BASICVALUE:
                print "type 0 to make lower cards have priority, and 1 to make higher cards have priority"
                newGreater = int(input())
                newGreater = False if newGreater == 0 else True
                
                rule = Rule(BASICVALUE, newGreater)
                makeModification(rule)
                
                return
                
            elif rule == WILDVALUE:
                print "type in a value between 2 and 14 to make that the new wild value"
                newValue = int(input())
                
                rule = Rule(WILDVALUE, newValue)
                makeModification(rule)
                
                return
                
            elif rule == WILDSUIT:
                while True:
                    print "type in S, D, C, or H to change your suit"
                    suit = raw_input().upper()
                    if len(suit) == 1 and suit in "SDCH":
                        
                        rule = Rule(WILDVALUE, suit)
                        makeModification(rule)
                        
                        return
                    else:
                        print "invalid character, try again"
        
        
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
        suits = ['H', 'D', 'C', 'S', None]
        self.all_states = []
        for basicValue in [True,False]:
            for i in [2,3,4,5,6,7,8,9,10,11,12,13,14, None]:
                for suit in suits:
                    for suit2 in suits:
                        self.all_states.append(State(Rule(BASICVALUE, basicValue), Rule(BASICSUIT, suit), Rule(WILDVALUE, i), Rule(WILDSUIT, suit2) ))
        
        for state in self.all_states:
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
        if notification.type == LEGAL:
            res = True
        elif notification.type == PENALTY:
            res = False
        else:
            return

        states_agree = []
        c = Checker()
        print notification.attemptedCard
        print notification.type
        for state in self.all_states:
            if c.isConsistent(notification, state) == res:
                states_agree.append(state)

        for state in states_agree:
            self.beliefs[state] += 5.0 / len(states_agree)

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
        pass # DO NOT CHANGE
