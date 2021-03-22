from Initializer import initSimulation
from MontecarloAgent import MontecarloPlayer
from Functions import selectionFunction, retropropagationFunction, movementChoiceFunction, expansionFunction, simulationFunction
import json
from Logic import Action

simulation = initSimulation()

history = {}

with open('history.json', 'r') as outfile:
    history = json.load(outfile)

historyActions = {}

for key in history:
    actionJsonDict = history.get(key)
    historyActions[key] = {}
    for actionKey in actionJsonDict:
        actionJson = actionJsonDict.get(actionKey)
        actionType = actionJson.get('type')
        stageId = actionJson.get('stageId')
        truckId = actionJson.get('truckId')

        action = Action(actionType, stageId, truckId)
        historyActions[key][actionKey] = action


for key in historyActions:
    actionsDict = historyActions.get(key)
    simulation.doActions(actionsDict)