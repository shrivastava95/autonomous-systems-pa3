import matplotlib.pyplot as plt
import networkx as nx
from nodes import vertices

print(vertices.split('\n').__len__() / 3)
lines = vertices.split('\n')
vertices = [[lines[3*i][1:-1], list(map(float,lines[3*i + 1].split()[:2]))] for i in range(len(lines) // 3)]

#######################################3


# Create a graph
G = nx.Graph()
# Add nodes with positions (example positions)
positions = {f'Node {vertices[i][0]}': vertices[i][1] for i in range(len(vertices))}
for node, pos in positions.items():
    G.add_node(node, pos=pos)

# Initial plot
fig, ax = plt.subplots()
nx.draw(G, pos=positions, with_labels=True, node_color='skyblue')

# Interactive function to add edges
def on_click(event):
    # Check if the click was on an axis and was a right-click (event.button == 3 for right-click)
    if event.inaxes != ax or event.button != 1:
        return
    # Find the nearest node
    distances = {n: ((event.xdata - pos[0])**2 + (event.ydata - pos[1])**2) for n, pos in positions.items()}
    closest_node = min(distances, key=distances.get)
    if "last_node" in on_click.__dict__ and on_click.last_node != closest_node:
        G.add_edge(on_click.last_node, closest_node)
        nx.draw(G, pos=positions, with_labels=True, node_color='skyblue', ax=ax)
        fig.canvas.draw()
    on_click.last_node = closest_node

# Connect the click event
fig.canvas.mpl_connect('button_press_event', on_click)
plt.show()
