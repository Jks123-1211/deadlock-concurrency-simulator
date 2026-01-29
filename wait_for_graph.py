import networkx as nx
import matplotlib.pyplot as plt


def visualize_wait_for_graph(graph, cycle=None):
    G = nx.DiGraph()

    # Add nodes and edges
    for u in graph:
        for v in graph[u]:
            G.add_edge(f"P{u}", f"P{v}")

    pos = nx.circular_layout(G)

    # Build cycle edges if a deadlock cycle exists
    cycle_edges = set()
    if cycle:
        for i in range(len(cycle)):
            u = f"P{cycle[i]}"
            v = f"P{cycle[(i + 1) % len(cycle)]}"
            cycle_edges.add((u, v))

    # Assign colors to edges
    edge_colors = []
    for edge in G.edges():
        if edge in cycle_edges:
            edge_colors.append("red")
        else:
            edge_colors.append("black")

    # Draw graph
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightblue",
        node_size=2000,
        edge_color=edge_colors,
        arrows=True,
        arrowsize=20
    )

    title = "Wait-For Graph Visualization"
    if cycle:
        title += " (Deadlock Cycle Highlighted)"
    else:
        title += " (No Deadlock)"

    plt.title(title)
    plt.show()
