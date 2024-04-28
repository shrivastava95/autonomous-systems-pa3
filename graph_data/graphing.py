import matplotlib.pyplot as plt
import networkx as nx
from nodes2 import vertices

print(vertices.split('\n').__len__() / 3)
lines = vertices.split('\n')
vertices = [[lines[3*i][1:-1], list(map(float,lines[3*i + 1].split()[:2]))] for i in range(len(lines) // 3)]
