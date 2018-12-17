from agents import *
from features import *

#NOTE: Inspired by PS3 QLearning framework -- THANK YOU BERKELEY!
class QLearner(Agent):
    def __init__(self, name):
        super(Agent, self).__init__(name)
        self.weights = Counter()
        self.combostate = None
        self.features = [Illegality, LowCount, HighCount, SizeofHand]
    def getQValue(self, state, action):
        """
        Q(s, a) = w_1 f_1 + w_2 f_2 + ... + w_n f_n
        """
        qValue = 0.0
        featuresToActivity = featureDict(self.features, state, action, self.combostate)
        for feature, featureActivity in featuresToActivity.iteritems():
            qValue = qValue + self.weights[feature] * featureActivity
        return qValue
    
    def update(self, state, action, nextState, reward):
        """
        updates the weights, in response to an episode
        
        for each self.weights[feature]:
            w_i = w_i + alpha * diff * featureActivity
                diff = reward + gamma * V(s') - Q(s, a)
                    NOTE: V(s') = max_a' Q(s', a')
        """
        diff = reward + self.discount * self.getStateValue(nextState) - self.getQValue(state, action)
        featuresToActivity = featureDict(self.features, state, action, self..combostate)
        for feature, featureActivity in features.iteritems():
            self.weights[feature] = self.weights[feature] + self.alpha * diff * featureActivity

    def getStateValue(self, state):
        """
        Given a state, tells you the value of that state -- primarily used in diff
        """
        return self.computeQVals(state, True)

    def getBestAction(self, state):
        """
        Given a state, tells you the best action you can take
        """
        return self.computeQVals(state, False)

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
    


#
