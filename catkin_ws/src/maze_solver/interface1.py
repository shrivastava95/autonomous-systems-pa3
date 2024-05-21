import heapq
import math

def calculate_distance(pos1, pos2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def dijkstra(graph, id1, id2):
    # Priority queue: stores tuples (distance, node_id)
    pq = []
    heapq.heappush(pq, (0, id1))
    
    # Distances dictionary
    distances = {node: float('inf') for node in graph}
    distances[id1] = 0
    
    # Previous nodes in optimal path from source
    previous_nodes = {node: None for node in graph}
    
    # Set of visited nodes to avoid processing twice
    visited = set()
    
    while pq:
        # Select the node with the smallest distance
        current_distance, current_node = heapq.heappop(pq)
        visited.add(current_node)
        
        # Process each "neighbor" of the current node
        for neighbor in graph[current_node]['children']:
            if neighbor in visited:
                continue
            new_distance = current_distance + calculate_distance(graph[current_node]['position'], graph[neighbor]['position'])
            
            # Only consider this new path if it's better
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (new_distance, neighbor))
                
    # Path reconstruction from id2 back to id1
    path = []
    step = id2
    if previous_nodes[step] is None:
        return "No path found"
    
    while step is not None:
        path.append(step)
        step = previous_nodes[step]
    
    return path[::-1]  # reverse the path

# Example graph structure
from graphdata import graph, get_id_from_name
import json


# Using the function to find the shortest path from 'A' to 'F'
print(get_id_from_name)
start_node = 'main_gate'
target_node = 'lhc'
start_node_id, target_node_id = [get_id_from_name[item] for item in [start_node, target_node]]

shortest_path = dijkstra(graph, start_node_id, target_node_id)
shortest_path_verbose = [graph[item]['name'] for item in shortest_path]
print(f"Shortest path from '{start_node}' to '{target_node}':", json.dumps(indent=4, obj=shortest_path_verbose))

# now, we execute the translation script for every pair of edges.

# shortest_path_verbose = [
#     "main_gate",
#     "id_113",
#     "id_102",
#     "id_100",
#     "knowledge_tree",
#     "id_117",
#     "academic_block",
#     "id_119",
#     "id_75",
#     "id_66",
#     "id_126",
#     "lhc"
# ]



import os
for i in range(len(shortest_path_verbose)-1):
    j = i + 1
    id_start = shortest_path_verbose[i]
    id_target = shortest_path_verbose[j]
    x, y = graph[get_id_from_name[id_target]]['position']
    os.system(f'python odom_test_4.py --target {x + 0.2} {y}')
    print(f'reached {shortest_path_verbose[j]}!')



