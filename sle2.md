# SLE-2 — BFS vs DFS Warehouse Search

## 1. Objective

SLE-2 studies how Breadth-First Search (BFS) and Depth-First Search (DFS) behave when searching a warehouse represented as a graph.

The experiment measures:

- execution time
- number of nodes explored

The work also uses `py-spy` for Python execution profiling.

---

## 2. Connection with Stockholm

The current Stockholm Inventory Agent uses BFS from `warehouse_search.py` to locate products.

SLE-2 was used to understand and compare BFS and DFS before choosing BFS for the agent's warehouse-location function.

The comparison itself is implemented separately in `search_experiment.py` so the experiment can use a larger test graph without changing the agent's runtime search module.

---

## 3. Warehouse Graph Used for the Experiment

`search_experiment.py` uses an 18-node warehouse graph.

```text
                         RECEIVING
                       /    |    |    |    \
                      /     |    |    |     \
                Storage-A Storage-B Storage-C Storage-D Storage-E
                  / | \      / | \     / \       / \       / \
               Rice Wheat Flour Oil Sugar Salt Tea Coffee Soap Shampoo Milk Butter
```

The experiment starts every search at:

```text
Receiving
```

Test targets are:

```text
Rice, Flour, Oil, Salt, Tea, Coffee, Soap, Butter
```

Each location/product is treated as a graph node and connections represent edges.

---

## 4. BFS — Breadth-First Search

BFS uses a queue and explores nodes level by level.

In the experiment, BFS starts from `Receiving`, explores reachable nodes and stops when it finds the target product.

BFS is also the algorithm used by the current Inventory Agent for product-location search.

---

## 5. DFS — Depth-First Search

DFS uses a stack and explores one branch before moving to another.

It is included in SLE-2 as the comparison algorithm. It is not currently used by the Inventory Agent for warehouse location.

---

## 6. Experiment Method

For each target product:

1. BFS searches from `Receiving`.
2. DFS searches from `Receiving`.
3. The number of nodes explored is recorded.
4. Execution time is measured with `timeit`.
5. Each timing uses 5 repeated measurements.
6. Each measurement performs 1,000 searches.

The experiment uses the same graph and target set for both algorithms.

---

## 7. Results

The recorded SLE-2 summary was:

| Metric | BFS | DFS |
|---|---:|---:|
| Average time | 7.7680 ms | 5.7796 ms |
| Total nodes explored | 98 | 89 |

These values are specific to the tested graph, targets and Python environment. They should not be interpreted as a general statement that DFS is always faster than BFS.

The important project outcome is that the experiment provided a direct comparison of the two search methods and helped connect the search study to the warehouse-search part of Stockholm.

---

## 8. Profiling with py-spy

`py-spy` was used to sample Python execution and generate a flamegraph for a longer workload.

Example commands:

```bash
python search_experiment.py bfs
python search_experiment.py dfs
```

Then profile the selected workload with:

```bash
py-spy record -o sle2_profile.svg -- python search_experiment.py bfs
```

The generated SVG is a profiling artifact rather than part of the Inventory Agent's runtime code.

---

## 9. Current Project Integration

The current Inventory Agent calls:

```python
bfs(
    self.warehouse,
    "Receiving",
    search_name
)
```

This means the SLE-2 search work is directly connected to the current Stockholm agent through `search_location()`.

---

## 10. Running the Experiment

Normal BFS vs DFS comparison:

```bash
python search_experiment.py
```

Dedicated profiling workloads:

```bash
python search_experiment.py bfs
python search_experiment.py dfs
```

---

## 11. Conclusion

SLE-2 provided practical experience with graph search, BFS, DFS, execution-time measurement and Python profiling. The result was then used in Stockholm's current design: BFS is the warehouse-location search used by the Inventory Agent.
