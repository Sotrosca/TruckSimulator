from MontecarloAgent import selectionFunction, Node
import random
import unittest

class Test(unittest.TestCase):

    def setUp(self):
        ids = iter(range(100))

        self.tree = Node(None, [], None, None, int(ids.__next__()))

        self.tree.visits = 1

        for i in range(3):
            child = Node(self.tree, [], None, None, int(ids.__next__()))
            child.value = (i + 1)
            child.visits = (i + 1) ** 2
            self.tree.childs.append(child)


        for j, _child in enumerate(self.tree.childs):
            for k in range(4):
                child = Node(self.tree, [], None, None, int(ids.__next__()))
                child.value = (j + 1 + k)
                child.visits = (j + 1 + k) ** 0.5
                _child.childs.append(child)

    def testSelectionFunction(self):
        self.assertEqual(selectionFunction(self.tree).id, 7)

if __name__ == '__main__':
    unittest.main(verbosity=2)

