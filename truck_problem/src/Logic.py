GO_STAGE = "GO"
DO_NOTHING = "DO_NOTHING"
FINISH = "FINISH"

class SimulationLogic():
    def __init__(self, trucksDict, scenarioDict):
        self.trucksDict = trucksDict
        self.stagesByLevelDict = scenarioDict['stagesByLevelDict']
        self.stagesByIdDict = scenarioDict['stagesByIdDict']
        self.scenarioLevelQuantity = len(self.stagesByLevelDict)
        self.finishedTrucksDict = {}
        self.epochs = 0
        self.history = {}

    def sendTruckToStage(self, truck, stageId):
        self.stagesByIdDict.get(truck.stageId).dispatchTruck(truck)
        nextStage = self.stagesByIdDict[stageId]
        nextStage.addTruck(truck)
        truck.setNewStage(nextStage)

    def finishTruckTravel(self, truck):
        self.stagesByIdDict.get(truck.stageId).dispatchTruck(truck)
        self.trucksDict.pop(truck.id)
        self.finishedTrucksDict[truck.id] = truck
        truck.stage = "FINISH"

    def doActionTruck(self, truckId, action):
        if action.type == FINISH:
            self.finishTruckTravel(action.truck)
        elif action.type == GO_STAGE:
            self.sendTruckToStage(action.truck, action.stageId)

    def doActions(self, actionDict):
        for actionKey in actionDict:
            self.doActionTruck(actionKey, actionDict[actionKey])

    def runOneEpoch(self, actionDict):
        self.saveHistory(actionDict)
        self.doActions(actionDict)
        for stage in self.stagesByIdDict.values():
            stage.runOneEpoch()

        self.epochs += 1

    def saveHistory(self, actionDict):
        self.history[self.epochs] = actionDict

    def getAllPosibleActions(self):
        actions = {}
        for stage in self.stagesByIdDict.values():
            stageTrucksDict = stage.getTrucksEnabledToDispatch()
            for truck in stageTrucksDict.values():
                actions[truck.id] = []
                nextLevel = truck.stageLevel + 1
                nextLevelStages = self.stagesByLevelDict.get(nextLevel, None)
                if nextLevelStages == None:
                    actions.get(truck.id).append(Action(FINISH, None, truck))
                else:
                    for stage in nextLevelStages:
                        if stage.canReceiveTruck(truck):
                            actions.get(truck.id).append(Action(GO_STAGE, stage.id, truck))

                    actions.get(truck.id).append(Action(DO_NOTHING, truck.stageId, truck))

        return actions

    def isSimulationEnd(self):
        return len(self.trucksDict) == 0

class Action():
    def __init__(self, type, stageId, truck):
        self.type = type
        self.stageId = stageId
        self.truck = truck

    def __str__(self):
        return self.type + " - " + str(self.stageId)
