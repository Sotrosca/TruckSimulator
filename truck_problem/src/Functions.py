import random
import numpy as np
import copy

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

def expansionFunction(node):
    return not node.hasChilds()

def simulationFunction(actionNode):
    cant = 0
    _simulationCopy = copy.deepcopy(actionNode.simulationCopy)
    while not _simulationCopy.isSimulationEnd():

        if cant > 50:
            print(cant)

        possibleActions = _simulationCopy.getAllPosibleActionsByTruck()
        actions = {}
        for key in possibleActions:
            actions[key] = random.choice(possibleActions.get(key))
        _simulationCopy.runOneEpoch(actions)

        cant += 1

    return _simulationCopy

def retropropagationFunction(simulationFinished, actionNode):
    valueNode = simulationFinished.epochs

    actualNode = actionNode

    actualNode.visits += 1
    actualNode.value += valueNode

    while actualNode.hasParent():
        actualNode = actualNode.parent
        actualNode.visits += 1
        actualNode.value += valueNode

def movementChoiceFunction(treeNodes):
    bestChildVisits = 0
    bestChild = None

    for child in treeNodes.childs:
        if child.visits > bestChildVisits:
            bestChildVisits = child.visits
            bestChild = child

    return bestChild
