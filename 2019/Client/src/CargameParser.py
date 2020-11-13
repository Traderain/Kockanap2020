import numpy as np
import cv2
import random
import math
from collections import defaultdict

def ParseTrack(track, checkpoints):
    lines = track.splitlines()
    w = len(lines)
    h = len(lines[0])
    mat = np.zeros((w, h, 3), dtype = "uint8")
    for i, x in enumerate(lines):
        for j, y in enumerate(lines[i]):
            if y == '0':
                mat[i,j] = [0,0,0]
            else:
                mat[i,j] = [255,255,255]

    step = 20
    mat = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)
    mat = cv2.distanceTransform(mat, cv2.DIST_L2, 3)
    cv2.normalize(mat, mat, 0, 1.0, cv2.NORM_MINMAX)

    g = Graph()
    for y in range(0, w, step):
        for x in range(0, h, step):
            weight = (1.0 - mat[y,x]) * 1000
            #g.add_node(str(x) + str(y))
            if x != 0:
                g.add_edge(str(x) + ',' + str(y), str(x - step) + ',' + str(y), weight)
                #cv2.line(mat, (x, y), (x - step, y), (0,255,0), 4)
            if y != 0:
                g.add_edge(str(x) + ',' + str(y), str(x) + ',' + str(y - step), weight)
                #cv2.line(mat, (x, y), (x, y - step), (0,255,0), 4)
            if x != 0 and y != 0:
                g.add_edge(str(x) + ',' + str(y), str(x - step) + ',' + str(y - step), math.sqrt(2 * weight**2))
                #cv2.line(mat, (x, y), (x - step, y - step), (0,255,0), 4)
            if x != h and y != 0:
                g.add_edge(str(x) + ',' + str(y), str(x + step) + ',' + str(y - step), math.sqrt(2 * weight**2))
                #cv2.line(mat, (x, y), (x + step, y - step), (0,255,0), 4)
            '''if [x,y] in linecenter:
                if x != 0:
                    g.add_edge(str(x) + ',' + str(y), str(x - step) + ',' + str(y), 1)
                if y != 0:
                    g.add_edge(str(x) + ',' + str(y), str(x) + ',' + str(y - step), 1)
                if x != 0 and y != 0:
                    g.add_edge(str(x) + ',' + str(y), str(x - step) + ',' + str(y - step), 1)
                if x != w and y != 0:
                    g.add_edge(str(x) + ',' + str(y), str(x + step) + ',' + str(y - step), 1)'''
    
    mat = cv2.cvtColor(mat, cv2.COLOR_GRAY2BGR)

    linecenter = []
    for checkpoint in checkpoints.splitlines():
        if 'line' in checkpoint:
            coords = checkpoint.split("\"")
            x1, y1, x2, y2 = int(coords[1]), int(coords[3]), int(coords[5]), int(coords[7])
            cv2.line(mat, (x1, y1), (x2, y2), (0,255,0), 4)
            cv2.circle(mat, (int((x1+x2)/2), int((y1+y2)/2)), 2, (0,0,255), 4)
            linecenter.append([round((x1+x2)/2/step) * step, round((y1+y2)/2/step) * step])
    
    for i, [x,y] in enumerate(linecenter):
        if i == len(linecenter) - 1:
            x2, y2 = linecenter[0][0], linecenter[0][1]
        else:
            x2, y2 = linecenter[i+1][0], linecenter[i+1][1]
        res = dijsktra(g, str(x) + ',' + str(y), str(x2) + ',' + str(y2))
        color = (random.uniform(0, 1.0), random.uniform(0, 1.0), random.uniform(0, 1.0))
        if res != 'Route Not Possible':
            for item in res:
                xy = item.split(',')
                x = int(xy[0])
                y = int(xy[1])
                cv2.circle(mat, (x, y), 2, color, 4)
    
    cv2.imshow('image', mat)
    cv2.waitKey(100)


class Graph():
    def __init__(self):
        """
        self.edges is a dict of all possible next nodes
        e.g. {'X': ['A', 'B', 'C', 'E'], ...}
        self.weights has all the weights between two nodes,
        with the two nodes as a tuple as the key
        e.g. {('X', 'A'): 7, ('X', 'B'): 2, ...}
        """
        self.edges = defaultdict(list)
        self.weights = {}
    
    def add_edge(self, from_node, to_node, weight):
        # Note: assumes edges are bi-directional
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight
    
def dijsktra(graph, initial, end):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()
    
    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)
        
        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
    
    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path