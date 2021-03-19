from Initializer import initSimulation
from MontecarloAgent import MontecarloPlayer
from Functions import selectionFunction, retropropagationFunction, movementChoiceFunction, expansionFunction, simulationFunction

simulation = initSimulation()

player = MontecarloPlayer(simulation, selectionFunction, expansionFunction, retropropagationFunction, simulationFunction, movementChoiceFunction)

bestMove = player.getBestMove()

print(bestMove)
