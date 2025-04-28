import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from networkx.generators.atlas import graph_atlas_g
from pycliques.cliques import clique_graph
from pycliques.lists import graph_generator
import copy


def is_clique_critical(graph):
    """
    Checks if a graph is clique-critical.
    """
    if not isinstance(graph, nx.Graph):
        raise TypeError(
            "Input must be a networkx graph.")

    this_clique_graph = clique_graph(graph)
    for vertex in graph.nodes():
        graph_vertex_removed = copy.deepcopy(graph)
        graph_vertex_removed.remove_node(vertex)
        removed_clique_graph = clique_graph(
            graph_vertex_removed)
        if nx.is_isomorphic(this_clique_graph,
                            removed_clique_graph):
            return False, None
    return True, this_clique_graph


def classify_graph(graph):
    """
    Classifies a graph against the graph atlas.
    """
    if not isinstance(graph, nx.Graph):
        raise TypeError(
            "Input must be a NetworkX graph object")
    if graph.order() <= 7:
        for index, listed_graph in enumerate(
                graph_atlas_g()):
            if nx.is_isomorphic(graph, listed_graph):
                return index
    return None


def plot_graph_classification(classification,
                              filename="graph_table.pdf",
                              graphs_per_page=6):
    """
    Plots graphs to a PDF, limiting graphs per page.
    Returns a sorted dictionary of the classification.
    """
    # Sort the classification by keys
    sorted_classification = dict(sorted(classification.items()))

    with PdfPages(filename) as pdf:
        for category, graphs in sorted_classification.items():
            num_graphs = len(graphs)
            start = 0
            while start < num_graphs:
                end = min(start + graphs_per_page, num_graphs)
                graphs_to_plot = graphs[start:end]
                num_cols = len(graphs_to_plot)

                fig, axes = plt.subplots(1, num_cols,
                                         figsize=(num_cols * 3, 3))

                if num_cols == 1:
                    axes = np.array([axes])

                for j, graph in enumerate(graphs_to_plot):
                    ax = axes[j]  # Access the subplot
                    nx.draw(graph, ax=ax, with_labels=False,
                            node_size=100)
                    ax.set_title(f"{category} - Graph {j+1}")

                plt.tight_layout()
                pdf.savefig(fig)
                plt.close(fig)
                start = end

    return sorted_classification


def process_graphs(graph_list, classification, check_connected=True):
    """
    Process a list of graphs and classify them if they're clique-critical.

    Args:
        graph_list: Iterable of graphs to process
        classification: Dictionary to store the classification
        check_connected: Whether to check if graphs are connected
        (default: True)
    """
    for graph in graph_list:
        if check_connected and not nx.is_connected(graph):
            continue
        is_critical, the_clique_graph = is_clique_critical(graph)
        if is_critical and len(the_clique_graph) <= 5:
            index = classify_graph(the_clique_graph)
            if index in classification:
                classification[index].append(graph)
            else:
                classification[index] = [graph]
    return classification


def main():
    """
    Main function to generate and plot the classification.
    """
    classification = {}
    plot_graph_classification(classification)
    process_graphs(nx.graph_atlas_g()[1:], classification)
    process_graphs(graph_generator(8), classification, check_connected=False)
    process_graphs(graph_generator(9), classification, check_connected=False)
    process_graphs(graph_generator(10), classification, check_connected=False)


if __name__ == '__main__':
    main()
