import pytest
import dijkstra

def parse_edges(edges):
    graph = {}
    for edge in edges:
        assert type(edge) is str
        graph[(edge[0], edge[1])] = float(edge[2:])
    return graph

def parse_graph(edges):
    graph = dijkstra.Digraph()
    for (frm, to), dist in parse_edges(edges).items():
        graph.addEdge(frm, to, dist)
    return graph

def parse_result(result):
    dist, path = result
    return dist, list(path)

maps = [
    ["AB7","AC4","AG3","BA7","BC3","BD5","CE8","CF6","DF40","ED15","FA3","GA3"]
]

dijkstra_test = {
    # graph, (from, to): (dist, path)
    (0, ("A", "D")): (12, "ABD"),
    (0, ("D", "A")): (43, "DFA"),
    (0, ("D", "E")): (55, "DFACE")
}

def list_all():
    for (n, params), out in dijkstra_test.items():
        graph = parse_graph(maps[n])
        out = parse_result(out)
        yield (graph, params, out)

@pytest.mark.parametrize("graph,params,out", list_all())
def test_min_path(graph, params, out):
    print(graph.dist)
    expected_dist, expected_path = out
    dist, path = graph.min_path(*params)
    assert dist == expected_dist, "incorrect distance"
    assert path == expected_path, "incorrect path"
