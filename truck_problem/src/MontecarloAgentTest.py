from MontecarloAgent import getActions
from Initializer import initSimulation
import unittest

class MontecarloAgentTest(unittest.TestCase):

    def setUp(self):
        self.simulation = initSimulation()
        self.truckQuantity = len(self.simulation.trucksDict)
        self.possibleActionsByTruck = self.simulation.getAllPosibleActionsByTruck()

    def testGetActions(self):
        listActions = []
        getActions(self.possibleActionsByTruck, {}, listActions)
        self.assertEqual(2 ** self.truckQuantity, len(listActions))

if __name__ == '__main__':
    unittest.main(verbosity=2)


