import random
import sys
from collections import namedtuple

Card = namedtuple('Card', ['value', 'suit'])

# rule settings
Rule = namedtuple('Rule', ['rule', 'setting'])
BASICVALUE = 1
BASICSUIT = 2 # I don't think there's much we can do with this as of now
WILDVALUE = 3
WILDSUIT = 4


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
    
class Player(object):
    def __init__(self, name, isHuman=False):
        self.hand = []
        self.name = name
        self.isHuman = isHuman

    def __str__(self):
        return str(self.name)
    
    # gives a card back to a player
    def takeCard(self, card):
        if card != None:
            self.hand.append(card)
        else:
            print "takeCard: no card drawn"
    
    def showHand(self):
        for index, card in enumerate(self.hand):
            print "Index:", index, " -- ", card
        
    def won(self):
        return len(self.hand) == 0
            
    def clearHand(self, deck=None):
        """
        If there is a deck, return the card to it.
        Else, simply clear the hand
        """
        if (deck == None):
            self.hand = []
        else:
            for card in self.hand:
                deck.append(card)
    
    # THIS IS WHAT THE GAME CALLS TO ASK FOR A PLAYER'S ACTION
    # removes and returns a card
    def takeAction(self, lastCard):
        """
        the Game class calls this method on the player when it wants the player
        to submit a card for legality evaluation.
        the "last card" -- ie, the most recent faceup card -- is supplied as an argument.
        
        this method also handles modification of the player's "hand"
        
        returns the card that was chosen.
        """
        card = self.chooseCard(lastCard)
        self.hand.remove(card)
        return card
        
    # AGENT IMPLEMENTED METHOD
    # notified when the state of the game changes, allows for analysis opportunity (ie updating beliefs)
    def notify(self, notification, game):
        # print player.name, "was notified"
        pass
        
    def humanChoose(self, lastCard):
        while True:
            # show your hand
            print "the LAST CARD that was played was:", lastCard
            print "your hand is: \n"
            self.showHand()
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
            
        
        
    #AI METHOD HERE. Returns a card. DOES NOT REMOVE IT!
    def chooseCard(self, lastCard):
        if self.isHuman:
            return self.humanChoose(lastCard)
        else:
            return self.hand[0] # change this!

    def modifyRule(self, game):
        # choose a random rule to modify
        # modify it
        if not self.isHuman:
            rule = random.choice([BASICVALUE, WILDVALUE, WILDSUIT])
            #
            if rule == BASICVALUE:
                newGreater = random.choice([True, False])
                game.basicValueConstraint.modify(newGreater)
                self.updateBeliefOnModification(rule, newGreater)
                
            elif rule == WILDVALUE:
                newValue = random.choice([i + 2 for i in range(13)])
                game.wildValueEffect.modify(newValue)
                self.updateBeliefOnModification(rule, newValue)
            
            elif rule == WILDSUIT:
                newSuit = random.choice(["D", "H", "S", "C"])
                game.wildSuitEffect.modify(newSuit)
                self.updateBeliefOnModification(rule, newSuit)
                
        else: 
            while True:
                try:
                    print "congrats, you get to change a rule! Please be precise"
                    print "type the rule you want to change -- 1 for basicValue, 3 for WildValue, and 4 for WildSuit"
                    rule = int(input())
                    
                    if rule == BASICVALUE:
                        print "type 0 to make lower cards have priority, and 1 to make higher cards have priority"
                        newGreater = int(input())
                        newGreater = False if newGreater == 0 else True
                        game.basicValueConstraint.modify(newGreater)
                        return
                        
                    elif rule == WILDVALUE:
                        print "type in a value between 2 and 14 to make that the new wild value"
                        newValue = int(input())
                        game.wildValueEffect.modify(newValue)
                        return
                        
                    elif rule == WILDSUIT:
                        while True:
                            print "type in S, D, C, or H to change your suit"
                            suit = raw_input().upper()
                            if len(suit) == 1 and s in "SDCH":
                                game.wildSuitEffect.modify(suit)
                                return
                            else:
                                print "invalid character, try again"
                except:
                    print "Invalid entry, let's start fresh\n"
            
    
    #AI METHOD
    def updateBeliefOnModification(self, rule, value):
        """
        updates an AI agent's understanding of the world based on a new rule it
        just created.
        """
        pass




#tests

# basic player taking action
# d = Deck()
# p = Player("j", True)
# p.takeCard(d.drawCard())
# p.takeCard(d.drawCard())
# print p.takeAction()

    
    
    
    
    
#
