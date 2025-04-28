import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from networkx.generators.atlas import graph_atlas_g
from pycliques.cliques import clique_graph
from pycliques.lists import graph_generator
import copy
from typing import Dict, List, Tuple, Optional, Iterable
import sys


def is_clique_critical(graph: nx.Graph) -> Tuple[Optional[bool],
                                                 Optional[nx.Graph]]:
    """
    Checks if a graph is clique-critical, with early exit if the
    clique graph has > 5 cliques.
    Returns None if criticality is indeterminate.
    """
    this_clique_graph: Optional[nx.Graph] = clique_graph(graph, 5)

    if this_clique_graph is None:
        # Graph has more than 5 cliques; criticality is indeterminate
        return None, None

    for vertex in graph.nodes():
        graph_vertex_removed: nx.Graph = copy.deepcopy(graph)
        graph_vertex_removed.remove_node(vertex)
        removed_clique_graph: nx.Graph = \
            clique_graph(graph_vertex_removed)

        if nx.is_isomorphic(this_clique_graph,
                            removed_clique_graph):
            return False, None  # Not critical

    return True, this_clique_graph  # Critical


def classify_graph(graph: nx.Graph) -> Optional[int]:
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


def plot_graph_classification(classification: Dict[Optional[int],
                                                   List[nx.Graph]],
                              filename: str = "graph_table.pdf",
                              graphs_per_page: int = 6
                              ) -> Dict[Optional[int], List[nx.Graph]]:
    """
    Plots graphs to a PDF, limiting graphs per page.
    Returns a sorted dictionary of the classification.
    """
    # Sort the classification by keys
    sorted_classification: Dict[Optional[int],
                                List[nx.Graph]] = dict(
        sorted(classification.items()))

    with PdfPages(filename) as pdf:
        for category, graphs in sorted_classification.items():
            num_graphs: int = len(graphs)
            start: int = 0
            while start < num_graphs:
                end: int = min(start + graphs_per_page, num_graphs)
                graphs_to_plot: List[nx.Graph] = graphs[start:end]
                num_cols: int = len(graphs_to_plot)

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


def process_graphs(graph_list: Iterable[nx.Graph],
                   classification: Dict[Optional[int], List[nx.Graph]],
                   check_connected: bool = True
                   ) -> Dict[Optional[int], List[nx.Graph]]:
    """
    Process a list or generator of graphs and classify them if they're
    clique-critical, with a progress counter.  Does not require
    knowing the total number of graphs in advance.

    Args:
        graph_list: Iterable of graphs to process
        classification: Dictionary to store the classification
        check_connected: Whether to check if graphs are connected
        (default: True)
    """
    i: int = 0  # Initialize graph counter
    for graph in graph_list:
        i += 1
        if check_connected and not nx.is_connected(graph):
            continue
        is_critical, the_clique_graph = is_clique_critical(graph)
        if (is_critical and the_clique_graph is not None and
                len(the_clique_graph) <= 5):
            index: Optional[int] = classify_graph(the_clique_graph)
            if index in classification:
                classification[index].append(graph)
            else:
                classification[index] = [graph]

        # Print progress counter in place
        print(f"\rProcessing graph: {i}", end="")
        sys.stdout.flush()  # Ensure output is flushed immediately

    print()  # Print newline after loop is completed
    return classification


def main() -> None:
    """
    Main function to generate and plot the classification.
    """
    classification: Dict[Optional[int], List[nx.Graph]] = {}
    process_graphs(nx.graph_atlas_g()[1:], classification)
    process_graphs(graph_generator(8), classification,
                   check_connected=False)
    process_graphs(graph_generator(9), classification,
                   check_connected=False)
    process_graphs(graph_generator(10), classification,
                   check_connected=False)
    plot_graph_classification(classification)


if __name__ == '__main__':
    main()
