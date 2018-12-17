lastActionfrom agents import *
from features import *

def calculateReward(fstate, action, combo, nextFstate):
    if len(nextFstate.hand) == 0:
        # you won!
        return 15
    elif len(nextFstate.opponentHand) == 0:
        # you lost!
        return -15
            
    # if you lose cards, + reward. if you gain cards, - reward
    return len(fstate.hand) - len(nextFstate.hand)

#NOTE: Inspired by PSet 3 QLearning framework -- THANK YOU BERKELEY!
class QLearner(Agent):
    """
    In general:
    state : Fstate
    action : card
    """
    def __init__(self, name, features):
        super(Agent, self).__init__(name)
        self.weights = Counter()
        self.features = features
        for feature in features:
            self.weights[feature] = 0
            
        
        self.gameRef = None
        self.lastAction = None
        self.lastFstate = None
        self.combostate = None
        self.opponent = None
    
    def getQValue(self, fstate, action):
        """
        Q(s, a) = w_1 f_1 + w_2 f_2 + ... + w_n f_n
        """
        qValue = 0.0
        featuresToActivity = featureDict(self.features, fstate, action, self.combostate)
        for feature, featureActivity in featuresToActivity.iteritems():
            qValue = qValue + self.weights[feature] * featureActivity
        return qValue
    
    def update(self, fstate, action, nextFState, reward):
        """
        updates the weights, in response to an episode
        
        for each self.weights[feature]:
            w_i = w_i + alpha * diff * featureActivity
                diff = reward + gamma * V(s') - Q(s, a)
                    NOTE: V(s') = max_a' Q(s', a')
        """
        diff = reward + self.discount * self.getStateValue(nextFState) - self.getQValue(fstate, action)

        featuresToActivity = featureDict(self.features, fstate, action, self.combostate)
        for feature, featureActivity in features.iteritems():
            self.weights[feature] = self.weights[feature] + self.alpha * diff * featureActivity

    def getStateValue(self, fstate):
        """
        Given a state, tells you the value of that state -- primarily used in diff
        """
        return self.computeQVals(fstate, True)

    def getBestAction(self, fstate):
        """
        Given a state, tells you the best action you can take
        """
        return self.computeQVals(fstate, False)

    def computeQVals(self, state, doReturnState): #else, return the best action
        """
        takes a state, and a doReturnState boolean
            if doReturnState == True, then returns the value of that state
            else, returns the best action you can take, given a state
            
        value of state: V(S) = max_a Q(S, A)
        best action: state with best Q value.
        """
        valuesForActions = Counter()
        for action in self.getLegalActions(state):
            valuesForActions[action] = self.getQValue(state,action)
        if (returnStateValue):
            return valuesForActions[valuesForActions.argMax()]
        else:
            return valuesForActions.argMax()
        
    def getLegalActions(self, state):
        return state.hand
        # return a list of legal actions! -- ie, cards that can be played
    

    def chooseCard(self, lastCard, aggressive=False):
        #place where we set a state
        if not aggressive:
            currentFstate = Fstate(self.hand[:], lastCard, self.opponent.hand)
            # choose a card
            cardToPlay = random.choice(self.hand)
            
            #this is NOT our first move
            if self.lastFstate != None:
                # calcuate the reward and update
                reward = calculateReward(self.lastFstate, self.lastAction, self.combostate, currentFstate)
                self.update(self.lastFstate, self.lastAction, currentFstate, reward)            
            
            self.lastFstate = currentFstate
            self.lastAction = cardToPlay
            return cardToPlay
        else:
            return random.choice(self.hand)


    def notify(self, notification, game):
        # if I just played a card
        if notification.type == NEWROUND:
            
            self.gameRef = game
            self.combostate = game.getCombinedState()
            self.lastAction = None
            self.lastFstate = None
            
            # set the opponent
            for player in game.players:
                if player != self:
                    self.opponent = player
                    break
            
        if notification.type == WON:
            self.gameRef = None # to prevent circular reference counting
            
            #if we won
            if game.players[game.activePlayer] == self:
                finalFstate = Fstate(self.hand[:], game.lastCard, self.opponent.hand)
                reward = calculateReward(self.lastFstate, self.lastAction, self.combostate, self.currentFstate)
                self.update(self.lastFstate, self.lastAction, finalFstate, reward) 
            # else, someone else won
            else:
                
            


#
