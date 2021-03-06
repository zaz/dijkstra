# Zaz Brown
# Public Domain
"""An efficient algorithm to find shortest paths between nodes in a directed graph."""
from collections import defaultdict

INFINITY = 1e309

class Digraph(object):
    def __init__(self, nodes=[]):
        self.nodes = set()
        self.neighbors = defaultdict(set)
        self.dist = {}

    def addNode(self, *nodes):
        [self.nodes.add(n) for n in nodes]

    def addEdge(self, frm, to, d=INFINITY):
        self.addNode(frm, to)
        self.neighbors[frm].add(to)
        self.dist[ frm, to ] = d

    def dijkstra(self, start, maxD=INFINITY):
        """Returns a map of nodes to distance from start and a map of nodes to
        the neighboring node that is closest to start."""
        # total distance from origin
        tdist = defaultdict(lambda: INFINITY)
        tdist[start] = 0
        # neighbor that is nearest to the origin
        preceding_node = {}
        unvisited = set(self.nodes)

        while unvisited:
            current = unvisited.intersection(tdist.keys())
            if not current: break
            min_node = min(current, key=tdist.get)
            unvisited.remove(min_node)

            for neighbor in self.neighbors[min_node]:
                d = tdist[min_node] + self.dist[min_node, neighbor]
                if tdist[neighbor] > d and maxD >= d:
                    tdist[neighbor] = d
                    preceding_node[neighbor] = min_node

        return tdist, preceding_node

    def min_path(self, start, end, maxD=INFINITY):
        """Returns the minimum distance and path from start to end."""
        tdist, preceding_node = self.dijkstra(start, maxD)
        dist = tdist[end]
        backpath = [end]
        try:
            while end != start:
                end = preceding_node[end]
                backpath.append(end)
            path = list(reversed(backpath))
        except KeyError:
            path = None

        return dist, path

    def dist_to(self, *args): return self.min_path(*args)[0]
    def path_to(self, *args): return self.min_path(*args)[1]


def load_map(mapFilename):
    """Build a graph from a file with lines of the form: from to distance"""
    graph = Digraph()
    f = open(mapFilename)
    for line in f:
        args = line.split()
        if len(args) == 3:
            args[2] = float(args[2])
            graph.addEdge(*args)

    return graph
