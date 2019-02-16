from haversine import haversine
import json
import math
import numpy as np

import graph

naut_mile = 1.852 # nautical mile to km
cycle = naut_mile * math.pi * 2

# check distances of path segments
def path_dists(lat, long, stops, graph, path, clusts):
    totals = []
    
    for k in range(len(stops) - 1):
        # i to j - 1
        a = subpath_dist(stops[k], stops[k+1], graph, path, clusts)

        # base to i
        b = haversine((lat, long), clusts[stops[k]])

        # base to j - 1
        c = haversine((lat, long), clusts[stops[k+1]])

        totals += [a + b + c]

    return totals
        
# subpath distance inclusive of i but exclusive of j
def subpath_dist(i, j, graph, path, clusts):
    dist = cycle

    for i in range(i, j - 2):
        dist += graph[path[i]][path[i+1]]
        dist += cycle

    return dist

# compute location of base
def find_base(graph, path, clusts, guess=480):
    total = cycle

    stops = [0]
    array = []

    # loop
    i = 0
    while i < len(clusts) - 1:
        total += graph[path[i]][path[i+1]] + cycle - naut_mile

        if total >= guess:
            array += [clusts[path[i]]]
            stops += [i]
            
            i -= 1
            total = 0

        i += 1

    # last loop
    stops += [len(clusts) - 1]

    sum_lat = 0
    sum_long = 0
    for point in array:
        sum_lat += point[0]
        sum_long += point[1]

    # base should be average of stops
    return sum_lat / len(array), sum_long / len(array), stops

# trace path
def trace(order):
    vects = []

    # the last point does not require a path
    for i in range(len(order) - 1):
        x1, y1 = order[i]
        x2, y2 = order[i+1]

        # get metrics
        vect = [x2 - x1, y2 - y1]
        magn = haversine(order[i], order[i+1])
        unit = [vc / magn for vc in vect]
        disp = [uc * naut_mile for uc in unit]

        # first point, find exit location i.e. start
        if i == 0:
            vects += [[x1 + disp[0], y1 + disp[1]]]

        # for other points, find entry location
        vects += [[x2 - disp[0], y2 - disp[1]]]

    return vects

# run module
def run(file):
    path, clusts, weights = graph.run(file)
    order = [clusts[poi] for poi in path]
    
    vects = trace(order)

    # find and check base
    lat, long, stops = find_base(weights, path, clusts)
    dists = path_dists(lat, long, stops, weights, path, clusts)
    print(lat, long)

    # write solution to json
    with open("solution.json", "w") as write:
        soln = []

        i = 0
        for point in path:
            soln += [{"cluster": {"latitude": clusts[point][0],
                                  "longitude": clusts[point][1]},
                      "path": {"latitude": vects[i][0],
                               "longitude": vects[i][1]}}]
            i += 1

        write.write(json.dumps({"solution": soln}))

    # stopping points
    with open("subpaths.json", "w") as write:
        segs = []
        for i in range(len(stops) - 1):
            segs += [{"start": stops[i], "stop": stops[i+1],
                      "distance": dists[i]}]
        
        write.write(json.dumps({"subpaths": segs}))

    # return path, distance
    return vects, sum(dists)

if __name__ == "__main__":
    vects, dist = run("poi.csv")
