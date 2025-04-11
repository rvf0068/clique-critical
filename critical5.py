import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from networkx.generators.atlas import graph_atlas_g


def plot_graph_classification(classification,
                              filename="graph_table.pdf"):
    """
    Plots the graph classification dictionary to a PDF file,
    handling potential page overflow and sorting the keys.
    """
    num_rows = len(classification)
    if num_rows == 0:
        print("No graphs to plot.")
        return

    # Sort the keys (Atlas indices)
    sorted_indices = sorted(classification.keys())

    max_cols = max(len(classification[index])
                   for index in sorted_indices)

    with PdfPages(filename) as pdf:
        for index in sorted_indices:
            graphs = classification[index]
            # Create a new figure for each row
            fig, axes = plt.subplots(1, max_cols,
                                     figsize=(max_cols * 3, 3))

            for j, graph in enumerate(graphs):
                if max_cols == 1:
                    ax = axes
                else:
                    ax = axes[j]
                ax.set_title(f"Atlas {index}",
                             fontsize=16)  # Increased fontsize

                nx.draw(graph, ax=ax, with_labels=False,
                        node_size=300)  # Increased node_size

            # Clear any unused subplots:
            num_graphs = len(graphs)
            for j in range(num_graphs, max_cols):
                if max_cols == 1:
                  ax = axes
                  ax.axis('off')
                else:
                  ax = axes[j]
                  ax.axis('off')

            plt.tight_layout(pad=2.0)
            pdf.savefig(fig)  # Save the figure to PDF
            plt.close(fig)  # Close the figure to release memory


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

    plot_graph_classification(classification)


if __name__ == '__main__':
    main()


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
