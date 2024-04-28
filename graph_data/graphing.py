import matplotlib.pyplot as plt
import networkx as nx
from nodes import vertices

print(vertices.split('\n').__len__() / 3)
lines = vertices.split('\n')
vertices = [[lines[3*i][1:-1], list(map(float,lines[3*i + 1].split()[:2]))] for i in range(len(lines) // 3)]
vertices = {item[0]: item[1] for item in vertices}
