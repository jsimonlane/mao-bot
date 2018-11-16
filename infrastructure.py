import random

class Card(object):
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val

    def __cmp__(self, other): #allows use of "sorted" on a list of cards, which will compare them by VALUE
        if self.value < other.value:
            return -1
        elif self.value == other.value:
            return 0
        else:
            return 1
    
    #names the objects so that if you "print object", returns a string
    def __str__(self):
        text = ""
        if self.value == 11:
            text = "J"
        elif self.value == 12:
            text = "Q"
        elif self.value == 13:
            text = "K"
        elif self.value == 14:
            text = "A"
        else:
            text = str(self.value)

        text += self.suit 

        return text

    #a prettier way to view a card
    def show(self):
        print self

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
                self.cards.append(Card(s,v))

    def shuffle(self):
        random.shuffle(self.cards)

    def drawCard(self):
        return self.cards.pop() #removes the last card ("the top")

class Player(object):
    def __init__(self, name):
        self.hand = []
        self.name = name

    def __str__(self):
        return str(self.name)

    def draw(self, deck):
        """
        Draws from the deck supplied as an argument
        """
        self.hand.append(deck.drawCard())

    # it occurs to me now that this probably isn't the best way to pass cards
    def playCard(self, card):
        """
        removes and returns card if successful, None if fails
        """
        try:
            self.remove(card)
            return card
        except:
            return None
    
    def showHand(self):
        for card in self.hand:
            print(card)
            
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
