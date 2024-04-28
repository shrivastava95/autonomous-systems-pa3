from connections import connections

tours = connections.split('\n')
tours = [tour.split('-') for tour in tours]
tours = [['id_' + item.strip() for item in tour] for tour in tours]

from nodes import vertices
import numpy as np

print(vertices.split('\n').__len__() / 3)
lines = vertices.split('\n')
vertices = [[lines[3*i][1:-1], list(map(float,lines[3*i + 1].split()[:2]))] for i in range(len(lines) // 3)]
vertices = {item[0]: item[1] for item in vertices}

total = 0

for tour in tours:
    for i in range(len(tour)-1):
        j = i + 1
        vi = np.array(vertices[tour[i]])
        vj = np.array(vertices[tour[j]])
        total += np.sqrt(np.sum(np.square(vi - vj)))

print(total)