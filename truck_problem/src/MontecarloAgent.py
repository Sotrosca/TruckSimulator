import random
import copy

class MontecarloPlayer():
    def __init__(self, originalSimulation):
        self.originalSimulation = originalSimulation
        self.actionTree = Node(None, [], None)

    def chooseActions(self, possibleActionsDict):
        actions = {}
        for key in possibleActionsDict:
            actions[key] = random.choice(possibleActionsDict.get(key))
        return actions

    def simulateOneEpoch(self, actions):
        self.simulationCopy.runOneEpoch(actions)

    def runSimulation(self):
        self.logSimulationCopyState([], [])
        while (not self.simulationCopy.isSimulationEnd()) and self.simulationCopy.epochs < 10:
            possibleActions = self.simulationCopy.getAllPosibleActions()
            actions = self.chooseActions(possibleActions)
            self.simulateOneEpoch(actions)
            self.logSimulationCopyState(possibleActions, actions)
#        for key in self.simulationCopy.history:
#            print(str(key) + " - " + str(self.simulationCopy.history[key])

class Node():
    def __init__(self, parent, childs, action):
        self.parent = parent
        self.childs = childs
        self.action = action

