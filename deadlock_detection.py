def find_deadlock_cycle(graph):
    visited = set()
    stack = []
    cycle = []

    def dfs(node):
        visited.add(node)
        stack.append(node)

        for neigh in graph.get(node, []):
            if neigh not in visited:
                if dfs(neigh):
                    return True
            elif neigh in stack:
                idx = stack.index(neigh)
                cycle.extend(stack[idx:])
                return True

        stack.pop()
        return False

    for node in graph:
        if node not in visited:
            if dfs(node):
                return cycle

    return []


def recover_deadlock(graph):
    cycle = find_deadlock_cycle(graph)
    if not cycle:
        return False, None, graph

    victim = cycle[0]  # simple victim selection
    graph.pop(victim, None)

    for k in graph:
        if victim in graph[k]:
            graph[k].remove(victim)

    return True, victim, graph
def get_deadlock_cycle(graph):
    visited = set()
    stack = []

    def dfs(node):
        visited.add(node)
        stack.append(node)

        for neigh in graph.get(node, []):
            if neigh not in visited:
                if dfs(neigh):
                    return True
            elif neigh in stack:
                return stack[stack.index(neigh):]

        stack.pop()
        return False

    for node in graph:
        if node not in visited:
            result = dfs(node)
            if result:
                return result

    return None
