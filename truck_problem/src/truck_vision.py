import sys, pygame
import json
from Initializer import initSimulation

def loadActionDict(actionDictJSONFile):
    with open(actionDictJSONFile, 'r') as parametersFile:
        actionDict = json.load(parametersFile)

        return actionDict

size = width, height = 1000, 600

title = pygame.display.set_caption("Truck problem")
screen = pygame.display.set_mode(size)


simulation = initSimulation()
#simulation.history = loadActionDict('')

levelQuantity = 2 + len(simulation.stagesByLevelDict)

startFinishHeight = height - 10

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    
    rect = pygame.Rect((10, (height - startFinishHeight) / 2), (100, startFinishHeight))
    pygame.draw.rect(screen, (255, 255, 255), rect, 3)
    pygame.display.flip()