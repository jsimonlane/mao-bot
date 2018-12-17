from game import *
import pickle

 #  _______        _       _               __ 
 # |__   __|      (_)     (_)             /_ |
 #    | |_ __ __ _ _ _ __  _ _ __   __ _   | |
 #    | | '__/ _` | | '_ \| | '_ \ / _` |  | |
 #    | | | | (_| | | | | | | | | | (_| |  | |
 #    |_|_|  \__,_|_|_| |_|_|_| |_|\__, |  |_|
 #                                  __/ |     
 #                                 |___/      
featureSet1 = [SizeofHand(), HighCount(), LowCount(), Illegality()]

def printGameStats(g):
    for player in g.players:
        print player.name
        print player.wins
        if type(player) == LearningAgent or type(player) == RandomAgent or type(player) == HmmAgent or type(player) == HeuristicAgent:
            print np.average(player.validPercentByRound)
        if type(player) == QLearner:
            print player.weights
            print 'Training 1: pickled weights:', pickle.dumps(player.weights)

def train1():
    qBot1 = QLearner('qBot1', featureSet1) #default values
    pBot2 = HmmAgent("A2")
    
    random.seed(182)
    g = Game([qBot1, pBot2], True)
    try:
        g.playGame(5000)
        printGameStats(g)
    except:
        printGameStats(g)
    

# see output.py for the pickled output


featureSet3 = [SizeofHand(), HighCount(), LowCount(), Illegality(), SkipCount(), ScrewCount(), PoisonCount(), WildValue(), MajorityPercent(), WildSuit(), PlayScrew(), PlaySkip()]

def train3():
    qBot1 = QLearner('qBot1', featureSet3) #default values
    pBot2 = RandomAgent("A2")
    
    random.seed(182)
    g = Game([qBot1, pBot2], True)
    try:
        g.playGame(5000)
        printGameStats(g)
    except:
        printGameStats(g)

featureSet4 = featureSet3 #simply do more training

def train4():
    qBot1 = QLearner('qBot1', featureSet3) #default values
    pBot2 = RandomAgent("A2")
    
    random.seed(182)
    g = Game([qBot1, pBot2], True)
    try:
        g.playGame(10000)
        printGameStats(g)
    except:
        printGameStats(g)
        
        
featureSet5 = featureSet3
def train5():
    qBot1 = QLearner('QLearner', featureSet5) #default values
    pBot2 = HmmAgent("Hmm")
    
    random.seed(182)
    g = Game([qBot1, pBot2], True)
    try:
        g.playGame(10000)
        printGameStats(g)
    except:
        printGameStats(g)
        
train5()

# see output.py for the pickled output





#
