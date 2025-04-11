import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from networkx.generators.atlas import graph_atlas_g


def plot_graph_classification(classification,
                              filename="graph_table.pdf",
                              graphs_per_page=6):
    """
    Plots the graph classification dictionary to a PDF file,
    limiting the number of graphs per page.
    """
    sorted_indices = sorted(classification.keys())

    with PdfPages(filename) as pdf:
        for index in sorted_indices:
            graphs = classification[index]
            num_graphs = len(graphs)

            start = 0
            while start < num_graphs:
                end = min(start + graphs_per_page, num_graphs)
                graphs_to_plot = graphs[start:end]
                num_cols = len(graphs_to_plot)

                fig, axes = plt.subplots(1, num_cols,
                                         figsize=(num_cols * 3, 3))

                for j, graph in enumerate(graphs_to_plot):
                    # Handle the case where axes is a single Axes object
                    if isinstance(axes, np.ndarray):
                        ax = axes[j] if num_cols > 1 else axes
                    else:
                        ax = axes

                    ax.set_title(f"Atlas {index}", fontsize=10)
                    nx.draw(graph, ax=ax, with_labels=False,
                            node_size=100)

                # Turn off any unused subplots. Account for single subplot
                for j in range(num_cols, graphs_per_page):
                    # Handle the case where axes is a single Axes object
                    if isinstance(axes, np.ndarray):
                        if num_cols > 1:
                            ax = axes[j]
                        else:
                            continue  # only 1 subplot, nothing to clear
                    else:
                        break  # only 1 axes object, nothing to clear

                    ax.axis('off')

                plt.tight_layout(pad=2.0)
                pdf.savefig(fig)
                plt.close(fig)
                start = end


def main():
    """
    Main function to generate and plot the classification.
    """
    from pycliques.cliques import clique_graph
    from pycliques.lists import list_graphs
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

    classification = {}
    for graph in nx.graph_atlas_g()[1:]:
        if nx.is_connected(graph):
            is_critical, the_clique_graph = \
                is_clique_critical(graph)
            if is_critical and \
                    len(the_clique_graph) <= 5:
                index = classify_graph(the_clique_graph)
                if index in classification:
                    classification[index].append(graph)
                else:
                    classification[index] = [graph]
    for graph in list_graphs(8):
        is_critical, the_clique_graph = is_clique_critical(graph)
        if is_critical and len(the_clique_graph) <= 5:
            index = classify_graph(the_clique_graph)
            if index in classification:
                classification[index].append(graph)
            else:
                classification[index] = [graph]
    for graph in list_graphs(9):
        is_critical, the_clique_graph = is_clique_critical(graph)
        if is_critical and len(the_clique_graph) <= 5:
            index = classify_graph(the_clique_graph)
            if index in classification:
                classification[index].append(graph)
            else:
                classification[index] = [graph]

    plot_graph_classification(classification)


if __name__ == '__main__':
    main()
