"""
Generates and classifies clique-critical graphs
"""
import copy
import networkx as nx
from networkx.generators.atlas import graph_atlas_g
from pycliques.cliques import clique_graph
from pycliques.lists import list_graphs


def is_clique_critical(graph):
    """
    Checks if a graph is clique-critical and optionally
    returns its clique graph.

    Args:
        graph (nx.Graph): The input graph.

    Returns:
        tuple: (is_critical, clique_graph), where
               is_critical is a boolean indicating whether
               the graph is clique-critical, and clique_graph
               is the clique graph if is_critical is True,
               otherwise None.
    """
    if not isinstance(graph, nx.Graph):
        raise TypeError("Input must be a networkx graph.")

    this_clique_graph = clique_graph(graph)
    for vertex in graph.nodes():
        graph_vertex_removed = copy.deepcopy(graph)
        graph_vertex_removed.remove_node(vertex)
        removed_clique_graph = clique_graph(
            graph_vertex_removed)
        if nx.is_isomorphic(this_clique_graph,
                            removed_clique_graph):
            return False, None  # Not critical, no clique graph
    return True, this_clique_graph  # Critical, return clique graph


def classify_graph(graph):
    """
    Classifies a graph by comparing it to the graphs in the
    NetworkX graph atlas.

    Args:
        graph: The NetworkX graph to classify.

    Returns:
        The index of the isomorphic graph in the graph atlas,
        or None if no isomorphic graph is found (or if the
        graph has more than 7 nodes).
    """
    if not isinstance(graph, nx.Graph):
        raise TypeError("Input must be a NetworkX graph object")

    if graph.order() <= 7:
        for index, listed_graph in enumerate(graph_atlas_g()):
            if nx.is_isomorphic(graph, listed_graph):
                return index
    return None


def main():
    """
    Main function to classify clique-critical graphs.

    Considers connected graphs from the graph atlas
    (excluding the empty graph) whose clique graphs
    have at most 5 vertices.
    """
    classification = {}
    for graph in nx.graph_atlas_g()[1:]:
        if nx.is_connected(graph):
            is_critical, the_clique_graph = is_clique_critical(graph)
            if is_critical and len(the_clique_graph) <= 5:
                index = classify_graph(the_clique_graph)
                if index in classification:
                    classification[index].append(graph)
                else:
                    classification[index] = [graph]
    print(classification)


if __name__ == '__main__':
    main()
