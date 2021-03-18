from Model import Truck, Server
from Initializer import initSimulation
from MontecarloAgent import MontecarloPlayer, selectionFunction, Node
import random

ids = iter(range(100))

tree = Node(None, [], None, None, int(ids.__next__()))

tree.visits = 1

for i in range(3):
    child = Node(tree, [], None, None, int(ids.__next__()))
    child.value = (i + 100)
    child.visits = (i + 1) ** 2
    tree.childs.append(child)


for j, _child in enumerate(tree.childs):
    for k in range(4):
        child = Node(tree, [], None, None, int(ids.__next__()))
        child.value = (j + 1 + k)
        child.visits = (j + 1 + k) ** 0.5
        _child.childs.append(child)


print(str(selectionFunction(tree)))