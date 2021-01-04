from Model import Truck, Server
from Initializer import initSimulation
from RandomPlayer import RandomPlayer
import random

simulation = initSimulation()

player = RandomPlayer(simulation)

player.runSimulation()

print(player.simulationCopy.epochs)