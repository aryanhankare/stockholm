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


# Small warehouse graph: 18 nodes
warehouse_graph = {
    "Receiving": ["Storage-A", "Storage-B", "Storage-C", "Storage-D", "Storage-E"],

    "Storage-A": ["Receiving", "Rice", "Wheat", "Flour"],
    "Storage-B": ["Receiving", "Oil", "Sugar", "Salt"],
    "Storage-C": ["Receiving", "Tea", "Coffee"],
    "Storage-D": ["Receiving", "Soap", "Shampoo"],
    "Storage-E": ["Receiving", "Milk", "Butter"],

    "Rice": ["Storage-A"],
    "Wheat": ["Storage-A"],
    "Flour": ["Storage-A"],

    "Oil": ["Storage-B"],
    "Sugar": ["Storage-B"],
    "Salt": ["Storage-B"],

    "Tea": ["Storage-C"],
    "Coffee": ["Storage-C"],

    "Soap": ["Storage-D"],
    "Shampoo": ["Storage-D"],

    "Milk": ["Storage-E"],
    "Butter": ["Storage-E"]
}


test_cases = [
    "Rice",
    "Flour",
    "Oil",
    "Salt",
    "Tea",
    "Coffee",
    "Soap",
    "Butter"
]


print("\nBFS vs DFS - Stockholm Search Experiment")
print("-" * 100)

print(
    f"{'Graph Size':<12}"
    f"{'Target':<12}"
    f"{'BFS Nodes':<12}"
    f"{'DFS Nodes':<12}"
    f"{'BFS Time (ms)':<18}"
    f"{'DFS Time (ms)':<18}"
)

print("-" * 100)


total_bfs_time = 0
total_dfs_time = 0
total_bfs_nodes = 0
total_dfs_nodes = 0


for target in test_cases:

    bfs_path, bfs_nodes = bfs(
        warehouse_graph,
        "Receiving",
        target
    )

    dfs_path, dfs_nodes = dfs(
        warehouse_graph,
        "Receiving",
        target
    )

    # Each timing performs 1000 searches.
    bfs_runs = timeit.repeat(
        lambda: bfs(
            warehouse_graph,
            "Receiving",
            target
        ),
        repeat=5,
        number=1000
    )

    dfs_runs = timeit.repeat(
        lambda: dfs(
            warehouse_graph,
            "Receiving",
            target
        ),
        repeat=5,
        number=1000
    )

    bfs_time = (sum(bfs_runs) / 5) * 1000
    dfs_time = (sum(dfs_runs) / 5) * 1000

    total_bfs_time += bfs_time
    total_dfs_time += dfs_time

    total_bfs_nodes += bfs_nodes
    total_dfs_nodes += dfs_nodes

    print(
        f"{len(warehouse_graph):<12}"
        f"{target:<12}"
        f"{bfs_nodes:<12}"
        f"{dfs_nodes:<12}"
        f"{bfs_time:<18.4f}"
        f"{dfs_time:<18.4f}"
    )


print("-" * 100)

print(f"Average BFS time: {total_bfs_time / len(test_cases):.4f} ms")
print(f"Average DFS time: {total_dfs_time / len(test_cases):.4f} ms")

print(f"Total BFS nodes explored: {total_bfs_nodes}")
print(f"Total DFS nodes explored: {total_dfs_nodes}")

print("\nEach timing = average of 5 runs.")
print("Each run performs 1,000 searches on the same warehouse graph.")
