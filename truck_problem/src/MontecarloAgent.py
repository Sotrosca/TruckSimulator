import random
import copy
import numpy as np

class MontecarloPlayer():
    def __init__(self, originalSimulation, selectionFunction, expansionFunction, retropropagationFunction, simulationFunction, movementChoiceFunction):
        self.originalSimulation = originalSimulation
        self.actionTree = Node(None, self.initTreeNodes(), None, None)
        self.selectionFunction = selectionFunction
        self.expansionFunction = expansionFunction
        self.simulationFunction = simulationFunction
        self.retropropagationFunction = retropropagationFunction
        self.movementChoiceFunction = movementChoiceFunction

    def initTreeNodes(self):
        nodes = []
        actions = self.originalSimulation.getAllPosibleActions()

        for action in actions:
            simulationCopy = copy.deepcopy(self.originalSimulation)
            simulationCopy.runOneEpoch(action)
            nodes.append(Node(self.actionTree, [], action, simulationCopy))

        return actions

    def getBestMove(self, epochs=100):

        for epoch in range(epochs):

            actionNode = self.selectionFunction(self.actionTree)

            if (self.expansionFunction):
                newActions = actionNode.simulationCopy.getAllPosibleActions()

                for action in newActions:
                    simulationCopy = copy.deepcopy(actionNode.simulationCopy)
                    simulationCopy.runOneEpoch(action)
                    actionNode.childs.append(Node(actionNode, [], action, simulationCopy))

                actionNode = self.selectionFunction(actionNode)
            
            simulationFinished = self.simulationFunction(actionNode)

            self.retropropagationFunction(simulationFinished, self.actionTree)
        
        bestMove = self.movementChoiceFunction(self.actionTree)

        return bestMove

class Node():
    def __init__(self, parent, childs, action, simulationCopy, idNode):
        self.parent = parent
        self.childs = childs
        self.action = action
        self.simulationCopy = simulationCopy
        self.visits = 0
        self.value = 0
        self.id = idNode

    def __str__(self):
        return "Id: " + str(self.id) + " - " + "visits: " + str(self.visits) + " - " + "value: " + str(self.value)

    def hasChilds(self):
        return self.childs != None and len(self.childs) > 0

    def getChildsWithoutVisits(self):
        childsWithoutLove = []

        for child in self.childs:
            if child.visits == 0:
                childsWithoutLove.append(child)

        return childsWithoutLove


def selectionFunction(treeNodes):
    UCTConstant = 1
    selectedNode = treeNodes

    while selectedNode.hasChilds():
        childsWithoutLove = selectedNode.getChildsWithoutVisits()

        if len(childsWithoutLove) > 0:
            selectedNode = random.choice(childsWithoutLove)
        
        else:
            
            selectionValueUCT = 0
            winnerNode = None

            for child in selectedNode.childs:
                childSuccessRatio = child.value / child.visits

                logRatio = (np.log(selectedNode.visits) / child.visits) ** 0.5

                childValueUCT = childSuccessRatio + UCTConstant * logRatio

                if childValueUCT > selectionValueUCT:
                    selectionValueUCT = childValueUCT
                    winnerNode = child

            selectedNode = winnerNode

    return selectedNode

