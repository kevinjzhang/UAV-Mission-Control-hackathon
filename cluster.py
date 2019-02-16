from haversine import haversine
import math
import numpy as np

import parse

# constants
radius = 0.6 # kilometers

# cluster data points
def cluster(points):
    clusts = []
    points = [[point, 0] for point in points]

    # create cluster
    for i in range(len(points)):
        accx = points[i][0][0]
        accy = points[i][0][1]
        size = 1

        # join close points if point untagged
        if points[i][1] == 0:
            for j in range(i+1, len(points)):
                # if close enough, check if point untagged
                if haversine(points[i][0][:2], points[j][0][:2]) < radius and\
                   points[j][1] == 0:
                    # tag and join cluster
                    points[j][1] = 1
                    accx += points[j][0][0]
                    accy += points[j][0][1]
                    size += 1

            clusts += [[accx/size, accy/size]]

    return clusts

# create adjacency-matrix graph
def make_graph(clusts):
    size = len(clusts)
    graph = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            graph[i][j] = haversine(clusts[i], clusts[j])

    return graph

# run module
def run(file):
    coords, _ = parse.run(file)
    clusts = cluster(coords)
    
    return make_graph(clusts), clusts

if __name__ == "__main__":
    graph, clusts = run("poi.csv")
        
