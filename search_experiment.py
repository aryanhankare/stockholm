import timeit


def bfs(graph, start, target):
    queue = [[start]]
    visited = {start}
    nodes_explored = 0

    while queue:
        path = queue.pop(0)
        current = path[-1]
        nodes_explored += 1

        if current == target:
            return path, nodes_explored

        for neighbour in graph[current]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(path + [neighbour])

    return None, nodes_explored


def dfs(graph, start, target):
    stack = [[start]]
    visited = {start}
    nodes_explored = 0

    while stack:
        path = stack.pop()
        current = path[-1]
        nodes_explored += 1

        if current == target:
            return path, nodes_explored

        for neighbour in graph[current]:
            if neighbour not in visited:
                visited.add(neighbour)
                stack.append(path + [neighbour])

    return None, nodes_explored


# -----------------------------
# SMALL GRAPH - 9 NODES
# -----------------------------

small_graph = {
    "Receiving": ["Storage-A", "Storage-B"],
    "Storage-A": ["Receiving", "Rice", "Wheat"],
    "Storage-B": ["Receiving", "Oil", "Sugar"],
    "Rice": ["Storage-A", "Packing"],
    "Wheat": ["Storage-A", "Packing"],
    "Oil": ["Storage-B", "Packing"],
    "Sugar": ["Storage-B", "Packing"],
    "Packing": ["Rice", "Wheat", "Oil", "Sugar", "Dispatch"],
    "Dispatch": ["Packing"]
}


# -----------------------------
# MEDIUM GRAPH - 15 NODES
# -----------------------------

medium_graph = {
    **small_graph,

    "Storage-C": ["Receiving", "Dal", "Flour"],
    "Dal": ["Storage-C", "Packing"],
    "Flour": ["Storage-C", "Packing"],

    "Storage-D": ["Receiving", "Tea", "Coffee"],
    "Tea": ["Storage-D", "Packing"],
    "Coffee": ["Storage-D", "Packing"]
}

medium_graph["Receiving"] = [
    "Storage-A",
    "Storage-B",
    "Storage-C",
    "Storage-D"
]


# -----------------------------
# LARGE GRAPH - 21 NODES
# -----------------------------

large_graph = {
    **medium_graph,

    "Storage-E": ["Receiving", "Biscuits", "Spices"],
    "Biscuits": ["Storage-E", "Packing"],
    "Spices": ["Storage-E", "Packing"],

    "Storage-F": ["Receiving", "Salt", "Soap"],
    "Salt": ["Storage-F", "Packing"],
    "Soap": ["Storage-F", "Packing"]
}

large_graph["Receiving"] = [
    "Storage-A",
    "Storage-B",
    "Storage-C",
    "Storage-D",
    "Storage-E",
    "Storage-F"
]


# -----------------------------
# TEST CASES
# -----------------------------

test_cases = [
    ("Rice", small_graph),
    ("Wheat", small_graph),

    ("Oil", medium_graph),
    ("Sugar", medium_graph),
    ("Dal", medium_graph),

    ("Tea", large_graph),
    ("Biscuits", large_graph),
    ("Salt", large_graph),
    ("Dispatch", large_graph)
]


# -----------------------------
# EXPERIMENT
# -----------------------------

print("\nBFS vs DFS - Stockholm Search Experiment")
print("-" * 100)

print(
    f"{'Graph Size':<12}"
    f"{'Target':<12}"
    f"{'BFS Nodes':<12}"
    f"{'DFS Nodes':<12}"
    f"{'BFS Time (s)':<18}"
    f"{'DFS Time (s)':<18}"
)

print("-" * 100)


for target, graph in test_cases:

    # Find nodes explored
    bfs_path, bfs_nodes = bfs(
        graph,
        "Receiving",
        target
    )

    dfs_path, dfs_nodes = dfs(
        graph,
        "Receiving",
        target
    )

    # BFS: 5 independent runs
    bfs_runs = timeit.repeat(
        lambda: bfs(
            graph,
            "Receiving",
            target
        ),
        repeat=5,
        number=10000
    )

    # DFS: 5 independent runs
    dfs_runs = timeit.repeat(
        lambda: dfs(
            graph,
            "Receiving",
            target
        ),
        repeat=5,
        number=10000
    )

    # Average time per search
    bfs_time = sum(bfs_runs) / (5 * 10000)
    dfs_time = sum(dfs_runs) / (5 * 10000)

    graph_size = len(graph)

    print(
        f"{graph_size:<12}"
        f"{target:<12}"
        f"{bfs_nodes:<12}"
        f"{dfs_nodes:<12}"
        f"{bfs_time:<18.10f}"
        f"{dfs_time:<18.10f}"
    )


print("-" * 100)
print("Each timing result = average of 5 runs × 10,000 iterations.")