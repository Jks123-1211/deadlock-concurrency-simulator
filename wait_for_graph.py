import networkx as nx
import matplotlib.pyplot as plt


def visualize_wait_for_graph(graph, cycle=None):
    G = nx.DiGraph()

    # Add edges
    for u in graph:
        for v in graph[u]:
            G.add_edge(f"P{u}", f"P{v}")

    pos = nx.circular_layout(G)

    # Default edge colors
    edge_colors = "black"

    # Highlight deadlock cycle
    if cycle:
        cycle_edges = []
        for i in range(len(cycle)):
            u = f"P{cycle[i]}"
            v = f"P{cycle[(i + 1) % len(cycle)]}"
            cycle_edges.append((u, v))

        edge_colors = [
            "red" if edge in cycle_edges else "black"
            for edge in G.edges()
        ]

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightblue",
        node_size=2000,
        edge_color=edge_colors,
        arrows=True
    )

    plt.title("Wait-For Graph (Deadlock in RED)")
    plt.show()
