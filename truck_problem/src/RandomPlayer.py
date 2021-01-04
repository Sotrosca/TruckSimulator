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
        self.logSimulationCopyState([], [])
        while (not self.simulationCopy.isSimulationEnd()) and self.simulationCopy.epochs < 10:
            possibleActions = self.simulationCopy.getAllPosibleActions()
            actions = self.chooseActions(possibleActions)
            self.simulateOneEpoch(actions)
            self.logSimulationCopyState(possibleActions, actions)
#        for key in self.simulationCopy.history:
#            print(str(key) + " - " + str(self.simulationCopy.history[key])

    def logSimulationCopyState(self, possibleActions, actions):
        print("Epoca: " + str(self.simulationCopy.epochs))
        '''
        print("Possible actions: ")
        for keyTruckActionsList in possibleActions:
            for action in possibleActions[keyTruckActionsList]:
                print(str(keyTruckActionsList) + " - " + str(action))
        print("------------------")
        '''

        print("Acciones a realizar: ")
        for key in possibleActions:
            if actions[key].type == "GO":
                print(" - Enviar camion numero " + str(key) + " a '" + str(actions[key].truck.stage.name) + "'")
            elif actions[key].type == "FINISH":
                print(" - Finalizar recorrido del camion numero " + str(key))
            elif actions[key].type == "DO_NOTHING":
                print(" - Camion numero " + str(key) + " dejado en espera en '" + str(actions[key].truck.stage.name) + "'")

        print("------------------")

        print("Estado del escenario luego de las acciones realizadas: ")
        for key in self.simulationCopy.stagesByIdDict:
            stage = self.simulationCopy.stagesByIdDict.get(key)
            truckListString = ""
            if stage.type == "QUEUE":
                for truck in stage.truckList:
                    truckListString += str(truck.id) + ", "
                truckListString = truckListString[:-2]
            elif stage.type == "SERVER":
                if stage.truckOnService != None:
                    truckListString += str(stage.truckOnService.id)
            else:
                for truckKey in stage.truckDict:
                    truckListString += str(truckKey) + ", "
                truckListString = truckListString[:-2]

            print(  "- " + str(self.simulationCopy.stagesByIdDict.get(key)) + " - camiones: [" + truckListString + "]")
        print("------------------")

        print("Camiones finalizados: ")
        for truck in self.simulationCopy.finishedTrucksDict:
            print("FINALIZO: " + str(truck))
    
        print()
        print("******************")
        print()
        