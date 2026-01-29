def get_deadlock_cycle(graph):
    """
    Returns a list representing the deadlock cycle if found,
    otherwise returns None.
    """
    visited = set()
    stack = []

    def dfs(node):
        visited.add(node)
        stack.append(node)

        for neigh in graph.get(node, []):
            if neigh not in visited:
                cycle = dfs(neigh)
                if cycle:
                    return cycle
            elif neigh in stack:
                return stack[stack.index(neigh):]

        stack.pop()
        return None

    for node in graph:
        if node not in visited:
            cycle = dfs(node)
            if cycle:
                return cycle

    return None


def recover_deadlock(graph):
    """
    Detects deadlock and recovers by terminating one process
    involved in the cycle.
    """
    cycle = get_deadlock_cycle(graph)

    if not cycle:
        return False, None, graph

    victim = cycle[0]  # simple victim selection strategy

    # Remove victim process
    graph.pop(victim, None)

    # Remove all edges pointing to victim
    for p in graph:
        if victim in graph[p]:
            graph[p].remove(victim)

    return True, victim, graph
