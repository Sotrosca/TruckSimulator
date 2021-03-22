from Initializer import initSimulation
from MontecarloAgent import MontecarloPlayer
from Functions import selectionFunction, retropropagationFunction, movementChoiceFunction, expansionFunction, simulationFunction


simulation = initSimulation()

player = MontecarloPlayer(simulation, selectionFunction, expansionFunction, retropropagationFunction, simulationFunction, movementChoiceFunction)

while not simulation.isSimulationEnd():
    '''
    print(simulation.epochs)
    bestMove = player.getBestMove(epochs=100)
    child = player.getChildById(bestMove.id)
    actionDict = child.action
    simulation.runOneEpoch(actionDict)
    child.parent = None
    player.actionTree = child
    '''
    print(simulation.epochs)
    bestMove = player.getBestMove(epochs=100)
    child = player.getChildById(bestMove.id)
    actionDict = child.action
    simulation.runOneEpoch(actionDict)
    child.parent = None
    player = MontecarloPlayer(simulation, selectionFunction, expansionFunction, retropropagationFunction, simulationFunction, movementChoiceFunction)
    player.actionTree = child

print(simulation.epochs)


