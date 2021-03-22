from Initializer import initSimulation
from RandomPlayer import RandomPlayer

simulation = initSimulation()

player = RandomPlayer(simulation)

player.runSimulation()

print(player.simulationCopy.epochs)