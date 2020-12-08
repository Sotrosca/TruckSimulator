import random
import copy

class RandomPlayer():
    def __init__(self, originalSimulation):
        self.originalSimulation = originalSimulation
        self.simulationCopy = copy.deepcopy(originalSimulation)

    def chooseActions(self, possibleActionsDict):
        actions = {}
        for key in possibleActionsDict:
            actions[key] = random.choice(possibleActionsDict.get(key))
        return actions

    def simulateOneEpoch(self, actions):
        self.simulationCopy.runOneEpoch(actions)

    def runSimulation(self):
        while not self.simulationCopy.isSimulationEnd() and self.simulationCopy.epochs < 50:
            possibleActions = self.simulationCopy.getAllPosibleActions()
            actions = self.chooseActions(possibleActions)
            self.simulateOneEpoch(actions)
            self.logSimulationCopyState(possibleActions, actions)

    def logSimulationCopyState(self, possibleActions, actions):
        print("Epoch: " + str(self.simulationCopy.epochs))
        print("Possible actions: ")
        for keyTruckActionsList in possibleActions:
            for action in possibleActions[keyTruckActionsList]:
                print(str(keyTruckActionsList) + " - " + str(action))
        print("------------------")

        print("Actions: ")
        for key in possibleActions:
            print(str(key) + ": " + str(actions[key]))
        print("------------------")

        print("Stages: ")
        for key in self.simulationCopy.stagesByIdDict:
            print(str(key) + " - " + str(self.simulationCopy.stagesByIdDict.get(key)))
        print("------------------")

        print("Finalizados: ")
        for truck in self.simulationCopy.finishedTrucksDict:
            print("FINALIZO: " + str(truck))
        print("******************")