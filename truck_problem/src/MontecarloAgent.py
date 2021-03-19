import copy

class MontecarloPlayer():

    def __init__(self, originalSimulation, selectionFunction, expansionFunction, retropropagationFunction, simulationFunction, movementChoiceFunction):
        self.idsNodes = iter(range(10000))
        self.originalSimulation = originalSimulation
        self.actionTree = Node(None, None, None, copy.deepcopy(self.originalSimulation), 0)
        self.actionTree.childs = self.initTreeNodes()
        self.selectionFunction = selectionFunction
        self.expansionFunction = expansionFunction
        self.simulationFunction = simulationFunction
        self.retropropagationFunction = retropropagationFunction
        self.movementChoiceFunction = movementChoiceFunction

    def initTreeNodes(self):
        nodes = []
        actions = []
        posibleActionsByTruck = self.originalSimulation.getAllPosibleActionsByTruck()
        self.getActions(posibleActionsByTruck, {}, actions)
        for action in actions:
            simulationCopy = copy.deepcopy(self.originalSimulation)
            copyAction = self.getCopyAction(action, simulationCopy)
            simulationCopy.runOneEpoch(copyAction)
            nodes.append(Node(self.actionTree, [], copyAction, simulationCopy, self.idsNodes.__next__()))

        return nodes

    def getCopyAction(self, action, simulationCopy):
        copyAction = {}

        for truckActionKey in action:
            newAction = action.get(truckActionKey)
            newAction.truck = simulationCopy.trucksDict.get(truckActionKey)
            copyAction[truckActionKey] = newAction

        return copyAction

    def getBestMove(self, epochs=100):

        for epoch in range(epochs):
            print(epoch)
            actionNode = self.selectionFunction(self.actionTree)
            if (self.expansionFunction(actionNode)):
                newActions = []
                posibleActionsByTruck = actionNode.simulationCopy.getAllPosibleActionsByTruck()
                self.getActions(posibleActionsByTruck, {}, newActions)
                for action in newActions:
                    simulationCopy = copy.deepcopy(actionNode.simulationCopy)
                    copyAction = self.getCopyAction(action, simulationCopy)
                    simulationCopy.runOneEpoch(copyAction)
                    actionNode.childs.append(Node(actionNode, [], copyAction, simulationCopy, self.idsNodes.__next__()))

                actionNode = self.selectionFunction(actionNode)

            simulationFinished = self.simulationFunction(actionNode)

            self.retropropagationFunction(simulationFinished, actionNode)

        bestMove = self.movementChoiceFunction(self.actionTree)

        return bestMove

    def getActions(self, posibleActionsByTruckDict, actionDict, actionList):

        if len(posibleActionsByTruckDict) == 0:
            actionList.append(actionDict)

        else:
            posibleActionsByTruckDictAux = copy.deepcopy(posibleActionsByTruckDict)
            possibleActionsByTruckKeys = list(posibleActionsByTruckDictAux.keys())
            actionTruckKey = possibleActionsByTruckKeys[0]

            for actionTruck in posibleActionsByTruckDictAux.pop(actionTruckKey):
                actionTruckDict = copy.deepcopy(actionDict)
                actionTruckDict[actionTruckKey] = actionTruck
                getActions(posibleActionsByTruckDictAux, actionTruckDict, actionList)


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

    def hasParent(self):
        return self.parent != None


def getActions(posibleActionsByTruckDict, actionDict, actionList):

    if len(posibleActionsByTruckDict) == 0:
        actionList.append(actionDict)

    else:
        posibleActionsByTruckDictAux = copy.deepcopy(posibleActionsByTruckDict)
        possibleActionsByTruckKeys = list(posibleActionsByTruckDictAux.keys())
        actionTruckKey = possibleActionsByTruckKeys[0]

        for actionTruck in posibleActionsByTruckDictAux.pop(actionTruckKey):
            actionTruckDict = copy.deepcopy(actionDict)
            actionTruckDict[actionTruckKey] = actionTruck
            getActions(posibleActionsByTruckDictAux, actionTruckDict, actionList)




