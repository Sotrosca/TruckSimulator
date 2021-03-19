from Model import Truck, Road, Queue, Server, Start
from Logic import SimulationLogic
import json
import pathlib

INITIAL_SCENARIO_FILE_PATH = 'C:/Users/fserna/Documents/42/Personal/Desarrollo_Software/Proyectos Personales/TruckSimulator/truck_problem/init/simulationInitialScenario.json'
SHORT_INITIAL_SCENARIO_FILE_PATH = 'C:/Users/fserna/Documents/42/Personal/Desarrollo_Software/Proyectos Personales/TruckSimulator/truck_problem/init/shortInitialScenario.json'
TRES_COLAS_INITIAL_SCENARIO_FILE_PATH = 'C:/Users/fserna/Documents/42/Personal/Desarrollo_Software/Proyectos Personales/TruckSimulator/truck_problem/init/tresColasScenario.json'


def loadInitParametersGame(initialParametersJSONFile):
    with open(initialParametersJSONFile, 'r') as parametersFile:
        initialParameters = json.load(parametersFile)

        return initialParameters

def initScenario(initialParameters):
    start = Start()
    stagesByLevelDict = {0: [start]} # Etapas separadas por nivel
    stagesByIdDict = {0: start} # Etapas separadas por id

    for stageData in initialParameters['stagesStructure']:
        stageLevel = stageData['level']
        stagesByLevelDict[stageLevel] = []
        for stage in stageData['stages']:
            stageParsed = parseStage(stage, stageLevel)
            stagesByLevelDict[stageLevel].append(stageParsed)
            stagesByIdDict[stageParsed.id] = stageParsed

    return {"stagesByLevelDict": stagesByLevelDict, "stagesByIdDict": stagesByIdDict}


def initTrucks(initialParameters, stagesById):
    trucksDict = {}
    for truckData in initialParameters['trucks']:
        truckStage = stagesById[truckData['stageId']]
        truck = Truck(truckData['id'], truckData['type'], truckStage)
        trucksDict[truck.id] = truck
        truckStage.addTruck(truck)
    return trucksDict

def initSimulation():
    initialParameters = loadInitParametersGame(SHORT_INITIAL_SCENARIO_FILE_PATH)
    initialScenario = initScenario(initialParameters)
    initialTrucks = initTrucks(initialParameters, initialScenario['stagesByIdDict'])
    return SimulationLogic(initialTrucks, initialScenario)

def parseStage(stageDataDict, stageLevel):
    if stageDataDict['type'] == "ROAD":
        return Road(stageDataDict['id'], stageDataDict['name'], stageLevel, stageDataDict['delayExpectation'], stageDataDict['delayVariance'])
    elif stageDataDict['type'] == "QUEUE":
        return Queue(stageDataDict['id'], stageDataDict['name'], stageLevel, [], stageDataDict['queueLimit'])
    elif stageDataDict['type'] == "SERVER":
        return Server(stageDataDict['id'], stageDataDict['name'], stageLevel, 0, stageDataDict['delayExpectation'], stageDataDict['delayVariance'])
