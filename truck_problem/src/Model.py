import numpy as np

class Truck():
    def __init__(self, id, type, stage):
        self.id = id
        self.type = type
        self.stageType = stage.type # ROAD, QUEUE, SERVER, FINISH, START
        self.stageLevel = stage.level
        self.stageId = stage.id
        self.stage = stage
        self.timeToArriveNextNode = 0
        self.timeToFinishServerService = 0

    def __str__(self):
        return "Camion " + str(self.id)

    def goToRoad(self, road):
        self.stage = stage
        self.timeToArriveNextNode = road.delay
        self.stageType = 'ROAD'

    def goToQueue(self, queue):
        self.stage = stage
        self.stageType = 'QUEUE'

    def goToServer(self, server):
        self.server = server
        self.timeToFinishServerService = server.timeToFinishService
        self.stageType = 'SERVER'

    def finishTravel(self):
        self.stageType = 'FINISH'

    def getStage(self):
        return self.stage

    def setNewStage(self, stage):
        self.stage = stage
        self.stageType = stage.type # ROAD, QUEUE, SERVER, FINISH, START
        self.stageLevel = stage.level
        self.stageId = stage.id


class Road():
    def __init__(self, id, name, level, delayExpectation, delayVariance):
        self.id = id
        self.name = name
        self.level = level
        self.truckDict = {}
        self.delayExpectation = delayExpectation
        self.delayVariance = delayVariance
        self.delay = self.simulateTimeToArrive()
        self.type = "ROAD"
        self.trucksTimeOnRoadDict = {}
        self.trucksTimeToDispatchDict = {}

    def __str__(self):
        return str(self.id) + ": " +  self.name

    def addTruck(self, truck):
        self.truckDict[truck.id] = truck
        self.trucksTimeOnRoadDict[truck.id] = 0
        self.trucksTimeToDispatchDict[truck.id] = self.simulateTimeToArrive()

    def dispatchTruck(self, truck):
        self.truckDict.pop(truck.id)
        self.trucksTimeOnRoadDict.pop(truck.id)
        self.trucksTimeToDispatchDict.pop(truck.id)

    def simulateTimeToArrive(self):
        return np.random.normal(self.delayExpectation, self.delayVariance)

    def canReceiveTruck(self, truck):
        return True

    def getTrucksEnabledToDispatch(self):
        trucksToDispatch = {}
        for truckId in self.trucksTimeOnRoadDict:
            if self.trucksTimeOnRoadDict.get(truckId) >= self.trucksTimeToDispatchDict.get(truckId):
                trucksToDispatch[truckId] = self.truckDict.get(truckId)
        return trucksToDispatch

    def runOneEpoch(self):
        for truckId in self.trucksTimeOnRoadDict:
            self.trucksTimeOnRoadDict[truckId] += 1


class Queue():
    def __init__(self, id, name, level, truckList, queueLimit):
        self.id = id
        self.name = name
        self.level = level
        self.truckList = truckList
        self.trucksOnQueueQuantity = len(truckList)
        self.queueLimit = queueLimit
        self.type = "QUEUE"

    def __str__(self):
        return str(self.id) + ": " +  self.name

    def canReceiveTruck(self, truck):
        return self.trucksOnQueueQuantity < self.queueLimit

    def addTruck(self, truck):
        self.truckList.append(truck)
        self.trucksOnQueueQuantity += 1

    def dispatchTruck(self, truck):
        self.trucksOnQueueQuantity -= 1
        return self.truckList.pop(0)

    def isEmpty(self):
        return self.trucksOnQueueQuantity == 0

    def getTrucksEnabledToDispatch(self):
        if self.trucksOnQueueQuantity == 0:
            return {}
        
        truckToDispatch = self.truckList[0]

        return {truckToDispatch.id: truckToDispatch}

    def runOneEpoch(self):
        pass


class Server():
    def __init__(self, id, name, level, timeOnService, delayExpectation, delayVariance):
        self.id = id
        self.name= name
        self.level = level
        self.timeOnService = timeOnService
        self.delayExpectation = delayExpectation
        self.delayVariance = delayVariance
        self.timeToFinishService = self.simulateTimeToFinishService()
        self.truckOnService = None
        self.type = "SERVER"

    def __str__(self):
        return str(self.id) + ": " +  self.name

    def simulateTimeToFinishService(self):
        return np.random.normal(self.delayExpectation, self.delayVariance)

    def runOneEpoch(self):
        if not self.isEmpty():
            self.timeOnService += 1

    def isEmpty(self):
        return self.truckOnService == None

    def isReadyToDispatchTruck(self):
        return self.timeOnService >= self.timeToFinishService

    def dispatchTruck(self, truck):
        truck = self.truckOnService
        self.truckOnService = None
        self.timeOnService = 0
        self.timeToFinishService = self.simulateTimeToFinishService()
        return truck

    def addTruck(self, truck):
        self.truckOnService = truck

    def canReceiveTruck(self, truck):
        return self.truckOnService == None

    def getTrucksEnabledToDispatch(self):
        if self.isEmpty() or not self.isServiceFinished():
            return {}
        
        truckToDispatch = self.truckOnService
        
        return {truckToDispatch.id: truckToDispatch}

    def isServiceFinished(self):
        return self.timeOnService >= self.timeToFinishService

class Start():
    def __init__(self):
        self.id = 0
        self.level = 0
        self.name = "Playon"
        self.truckDict = {}
        self.type = "START"

    def __str__(self):
        return str(self.id) + ": " +  self.name

    def addTruck(self, truck):
        self.truckDict[truck.id] = truck

    def dispatchTruck(self, truck):
        self.truckDict.pop(truck.id)

    def getTrucksEnabledToDispatch(self):
        return self.truckDict

    def runOneEpoch(self):
        pass
