import json

import cluster

# values
infinity = float("inf")

# approximate tsp on adjacency matrix
def approx_tsp(graph):
    # choose root
    root = 0
    
    # minimum spanning tree
    tree = prim_mst(graph, root)

    # pre-order walk
    return pre_order(tree)

# nearest neighbour
def nearest_nb(graph):
    size = len(graph)
    skip = [True] * size
    path = [0]
    
    skip[0] = False
    min_index = 0
    k = 0

    for i in range(len(graph) - 1):
        minimum = 500 # max value
        for j in range(len(graph)):
            if k != j and graph[k][j] < minimum and skip[j]:
                minimum = graph[k][j]
                min_index = j

        k = min_index
        skip[k] = False
        path += [k]

    return path
    
# prim's mst
def prim_mst(graph, root):
    size = len(graph)
    distances = [infinity] * size
    parents = [None] * size
    skip = [False] * size

    # start from root
    distances[root] = 0
    parents[root] = -1 # special value

    # get closest vertex to tree
    for _ in range(size):
        # visit vertex
        _, u = index_min(distances, skip)
        if u is None:
            break

        skip[u] = True

        # connect closest vertex to tree
        for v in range(size):
            if graph[u][v] > 0 and not skip[v] and distances[v] > graph[u][v]:
                distances[v] = graph[u][v]
                parents[v] = u

    return parents

# get index of minimum element
def index_min(values, skip):
    min_value = infinity
    min_index = None

    for index, value in enumerate(values):
        if value < min_value and not skip[index]:
            min_value = value
            min_index = index

    return min_value, min_index

# pre-order walk of parent list
def pre_order(parents, skip=None, elem=-1):
    if skip is None:
        skip = [False] * len(parents)

    # find all values which match elem
    result = []
    indices = [index for index, value in enumerate(parents)
               if value == elem and not skip[index]]

    if len(indices) == 0:
        return result

    # visit indices
    skip[indices[0]] = True
    for index in indices:
        result += [index] + pre_order(parents, skip, index)
    return result

# make list unique
def unique(xs):
    ys = set()
    zs = []

    for x in xs:
        if x not in ys:
            ys.add(x)
            zs += [x]

    return zs

# run module
def run(file):
    graph, clusts = cluster.run(file)
    # path = unique(approx_tsp(graph))
    path = nearest_nb(graph)

    return path, clusts, graph

if __name__ == "__main__":
    path, clusts, graph = run("poi.csv")
    
