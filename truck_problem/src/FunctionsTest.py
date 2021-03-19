from MontecarloAgent import Node
from Functions import selectionFunction, retropropagationFunction, movementChoiceFunction, simulationFunction
import random
import unittest
from Initializer import initSimulation

class FunctionsTest(unittest.TestCase):

    def setUp(self):

        self.simulation = initSimulation()
        self.simulation.epochs = 20

        ids = iter(range(100))

        self.tree = Node(None, [], None, self.simulation, int(ids.__next__()))

        self.tree.visits = 1

        for i in range(3):
            child = Node(self.tree, [], None, None, int(ids.__next__()))
            child.value = (i + 1)
            child.visits = (i + 1) ** 2
            self.tree.childs.append(child)


        for j, _child in enumerate(self.tree.childs):
            for k in range(4):
                child = Node(_child, [], None, None, int(ids.__next__()))
                child.value = (j + 1 + k)
                child.visits = (j + 1 + k) ** 2
                _child.childs.append(child)

        self.nodeRetropropagation = self.tree.childs[0].childs[3]

    def testSelectionFunction(self):
        self.assertEqual(selectionFunction(self.tree).id, 4)

    def testRetropropagationFunction(self):

        retropropagationFunction(self.simulation, self.nodeRetropropagation)
        self.assertEqual(self.nodeRetropropagation.visits, 17)
        self.assertEqual(self.nodeRetropropagation.value, 24)
        self.assertEqual(self.nodeRetropropagation.parent.visits, 2)
        self.assertEqual(self.nodeRetropropagation.parent.value, 21)

    def testMovementChoiceFunction(self):
        bestChild = self.tree.childs[2]
        self.assertEqual(movementChoiceFunction(self.tree), bestChild)

    def testSimulationFunction(self):
        self.assertEqual(simulationFunction(self.tree).isSimulationEnd(), True)



if __name__ == '__main__':
    unittest.main(verbosity=2)

