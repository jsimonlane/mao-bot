from qOutput import *
from qTraining import *
from agents import *
from game import *
import pickle

random.seed(10)

def play1():
    pBot2 = RandomAgent("Hmm")
    # qBot1 = RandomAgent("random")
    qBot1 = QPlayer('qPlayer', featureSet1, pickle.loads(trainingWeights1), pBot2) #default values
    
    random.seed(183)
    g = Game([qBot1, pBot2], True)
    g.playGame(100)

    # #print stats
    for player in g.players:
        print player.name
        print player.wins
        if type(player) == LearningAgent or type(player) == RandomAgent or type(player) == HmmAgent or type(player) == HeuristicAgent or type(player) == QPlayer:
            print np.average(player.validPercentByRound)

def play2(agent):
    pBot2 = agent
    # qBot1 = RandomAgent("random")
    qBot1 = QPlayer('qPlayer', featureSet5, pickle.loads(trainingWeights5), pBot2) #default values
    
    random.seed(183)
    g = Game([qBot1, pBot2], True)
    g.playGame(100)

    # #print stats
    for player in g.players:
        print player.name
        print player.wins
        if type(player) == LearningAgent or type(player) == RandomAgent or type(player) == HmmAgent or type(player) == HeuristicAgent or type(player) == QPlayer:
            print np.average(player.validPercentByRound)


def play3():
    pBot2 = HmmAgent("Hmm")
    # qBot1 = RandomAgent("random")
    # qBot1 = QPlayer('qPlayer', featureSet5, pickle.loads(trainingWeights5), pBot2) #default values
    qBot1 = QCheater("QCheater", featureSet4, pickle.loads(trainingWeights7))
    
    random.seed(183)
    g = Game([qBot1, pBot2], True)
    
    g.playGame(100)

    # #print stats
    for player in g.players:
        print player.name
        print player.wins
        if type(player) == LearningAgent or type(player) == RandomAgent or type(player) == HmmAgent or type(player) == HeuristicAgent or type(player) == QPlayer:
            print np.average(player.validPercentByRound)
            
