# Zaz Brown
"""An efficient algorithm to find shortest paths between nodes in a graph."""
from collections import defaultdict

class Digraph(object):
    def __init__(self, nodes=[]):
        self.nodes = set()
        self.neighbours = defaultdict(set)
        self.dist = {}
        self.odist = {}

    def addNode(self, *nodes):
        [self.nodes.add(n) for n in nodes]

    def addEdge(self, frm, to, d=1e309, o=0):
        self.addNode(frm)
        self.addNode(to)
        self.neighbours[frm].add(to)
        self.dist[ frm, to ] = d
        self.odist[ frm, to ] = o

    def dijkstra(self, start, maxD=1e309, maxDO=1e309):
        """Returns a map of nodes to distance from start and a map of nodes to
        the neighbouring node that is closest to start."""
        # total distance from origin:
        tdist = defaultdict(lambda: 1e309)
        tdist[start] = 0
        tOdist = defaultdict(lambda: 1e309)
        tOdist[start] = 0
        preceding_node = {}

        nodes = self.nodes

        while nodes:
            current = nodes.intersection(tdist.keys())
            if not current: break
            min_node = min(current, key=tdist.get)

            nodes.remove(min_node)

            for neighbour in self.neighbours[min_node]:
                d  =  tdist[min_node] +  self.dist[min_node, neighbour]
                dO = tOdist[min_node] + self.odist[min_node, neighbour]
                if tdist[neighbour] > d and maxD >= d and maxDO >= dO:
                    tdist[neighbour] = d
                    tOdist[neighbour] = dO
                    preceding_node[neighbour] = min_node

        return tdist, preceding_node

    def min_path(self, start, end, maxD=1e309, maxDO=1e309):
        tdist, preceding_node = self.dijkstra(start, maxD, maxDO)
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

    def path_to(start, end, maxD=1e309, maxDO=1e309):
        return self.min_path(start, end, maxD, maxDO)[1]

    def dist_to(start, end, maxD=1e309, maxDO=1e309):
        return self.min_path(start, end, maxD, maxDO)[0]


def load_map(mapFilename):
    """Build a graph from a file with lines of the form: from to weight"""
    graph = Digraph()
    f = open(mapFilename)
    for line in f:
        args = line.split()
        if len(args) == 3:
            args[2] = float(args[2])
            graph.addEdge(*args)

    return graph
