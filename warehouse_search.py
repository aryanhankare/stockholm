def bfs(graph, start, target):
    queue = [[start]]
    visited = {start}

    while queue:
        path = queue.pop(0)
        current = path[-1]

        if current == target:
            return path

        for neighbour in graph[current]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(path + [neighbour])

    return None