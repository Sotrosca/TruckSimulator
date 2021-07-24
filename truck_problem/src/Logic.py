import json

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

    def writeJsonHistory(self, fileName):
        history = self.history
        jsonDict = {}

        for key in history:
            jsonDict[key] = {}
            epochActions = history.get(key)
            for actionKey in epochActions:
                actionDict = {}
                action = epochActions.get(actionKey)
                actionDict["type"] = action.type
                actionDict["stageId"] = action.stageId
                actionDict["truckId"] = action.truckId
                jsonDict[key][actionKey] = actionDict

        with open(fileName, 'w') as outfile:
            json.dump(jsonDict, outfile, indent=4, sort_keys=True)

    def readJsonHistory(self, fileName):
        history = {}

        with open(fileName, 'r') as outfile:
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
        return historyActions

    def sendTruckToStage(self, truckId, stageId):
        truck = self.trucksDict.get(truckId)
        self.stagesByIdDict.get(truck.stageId).dispatchTruck(truck)
        nextStage = self.stagesByIdDict.get(stageId)
        nextStage.addTruck(truck)
        truck.setNewStage(nextStage)

    def finishTruckTravel(self, truckId):
        truck = self.trucksDict.get(truckId)
        self.stagesByIdDict.get(truck.stageId).dispatchTruck(truck)
        self.trucksDict.pop(truck.id)
        self.finishedTrucksDict[truck.id] = truck
        truck.stage = "FINISH"

    def doActionTruck(self, truckId, action):
        if action.type == FINISH:
            self.finishTruckTravel(action.truckId)
        elif action.type == GO_STAGE:
            self.sendTruckToStage(action.truckId, action.stageId)

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

    def getAllPosibleActionsByTruckTypeOnStage(self):
        actions = {}
        for stage in self.stagesByIdDict.values():
            stageTrucksDict = stage.getTrucksEnabledToDispatch()
            truckQuantityByTypeDict = self.getTruckQuantityByTypeDict(stageTrucksDict)
            actions[stage.id] = truckQuantityByTypeDict

        return actions


    def getTruckQuantityByTypeDict(truckList):
        truckQuantityByTypeDict = {}
        for truck in truckList:
            if truckQuantityByTypeDict.has_key(truck.type):
                truckQuantityByTypeDict[truck.type] += 1
            else:
                truckQuantityByTypeDict[truck.type] = 1

        return truckQuantityByTypeDict

    def getAllPosibleActionsByTruck(self):
        actions = {}
        for stage in self.stagesByIdDict.values():
            stageTrucksDict = stage.getTrucksEnabledToDispatch()
            for truck in stageTrucksDict.values():
                actions[truck.id] = []
                nextLevel = truck.stageLevel + 1
                nextLevelStages = self.stagesByLevelDict.get(nextLevel, None)
                if nextLevelStages == None:
                    actions.get(truck.id).append(Action(FINISH, None, truck.id))
                else:
                    for stage in nextLevelStages:
                        if stage.canReceiveTruck(truck):
                            actions.get(truck.id).append(Action(GO_STAGE, stage.id, truck.id))

                    actions.get(truck.id).append(Action(DO_NOTHING, truck.stageId, truck.id))

        return actions

    def isSimulationEnd(self):
        return len(self.trucksDict) == 0

class Action():
    def __init__(self, actionType, stageId, truckId):
        self.type = actionType
        self.stageId = stageId
        self.truckId = truckId

    def __str__(self):
        return self.type + " - " + str(self.stageId)


    def toDict(self):
        jsonDict = {}

        jsonDict["type"] = self.type
        jsonDict["stageId"] = self.stageId
        jsonDict["truckId"] = self.truckId
