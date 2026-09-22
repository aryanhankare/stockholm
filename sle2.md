# Stockholm

**Stockholm** is an inventory and invoice management project being developed as a learning project.

The project combines inventory management, invoicing, and an initial inventory agent. It also includes a warehouse-search experiment used to compare **BFS (Breadth-First Search)** and **DFS (Depth-First Search)** as part of SLE-2.

---

## Project Overview

Stockholm currently includes:

* Invoice generator frontend
* Inventory management prototype
* Rule-based inventory agent
* Warehouse graph and product search
* BFS vs DFS performance experiment
* AI Contribution Log for SLE-1

The long-term goal is to connect the inventory system with an intelligent agent that can analyse stock and make useful inventory decisions.

---

## Inventory Agent

The current inventory agent follows a basic:

**Perceive → Decide → Act**

cycle.

It checks product quantities against a low-stock threshold and produces one of three decisions:

| Decision       | Condition                                       |
| -------------- | ----------------------------------------------- |
| `OUT_OF_STOCK` | Quantity is 0 or below                          |
| `REORDER`      | Quantity is at or below the low-stock threshold |
| `NO_ACTION`    | Stock is above the threshold                    |

The agent is currently a Python prototype and is not yet connected to the web application or a database.

---

## Warehouse Graph

For the search experiment, the warehouse is represented as a **graph**.

* `Receiving` is the starting point.
* `Storage-A` to `Storage-E` represent storage sections.
* Products are connected to their respective storage sections.
* Each location/product is treated as a **node**.
* Connections between nodes represent **edges**.

### Warehouse Layout

```text
                         ┌─────────────┐
                         │  RECEIVING  │
                         └──────┬──────┘
                                │
       ┌────────────┬───────────┼───────────┬────────────┐
       │            │           │           │            │
       ▼            ▼           ▼           ▼            ▼
┌────────────┐ ┌────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ STORAGE-A  │ │ STORAGE-B  │ │STORAGE-C │ │STORAGE-D │ │STORAGE-E │
└─────┬──────┘ └─────┬──────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘
      │               │             │             │             │
  ┌───┼───┐       ┌───┼───┐      ┌──┼──┐       ┌──┼──┐       ┌──┼──┐
  ▼   ▼   ▼       ▼   ▼   ▼      ▼     ▼       ▼     ▼       ▼     ▼
Rice Wheat Flour  Oil Sugar Salt Tea Coffee   Soap Shampoo   Milk Butter
```

This is the same warehouse structure used in `search_experiment.py`.

---

## BFS vs DFS Search

The warehouse graph is used to compare two search algorithms.

### BFS — Breadth-First Search

BFS uses a **queue** and explores the graph level by level.

```text
BFS
 │
 └── Queue
      │
      └── Level-by-level search
```

### DFS — Depth-First Search

DFS uses a **stack** and explores one branch deeply before moving to another.

```text
DFS
 │
 └── Stack
      │
      └── Deep-first search
```

Both algorithms start from:

```text
Receiving
```

and search for a target product such as:

```text
Rice, Flour, Oil, Salt, Tea, Coffee, Soap, Butter
```

---

## SLE-2 Performance Experiment

The SLE-2 experiment compares BFS and DFS using the **same warehouse graph and the same target products**.

The experiment measures:

* Execution time
* Number of nodes explored

### Results

| Metric               |       BFS |       DFS |
| -------------------- | --------: | --------: |
| Average time         | 7.7680 ms | 5.7796 ms |
| Total nodes explored |        98 |        89 |

Each timing is the average of **5 runs**, with each run performing **1,000 searches** on the same warehouse graph.

For this particular graph and test cases, DFS produced a lower average execution time and explored fewer total nodes. This result is specific to the tested warehouse structure and does not mean DFS is always faster than BFS.

---

## Profiling

The experiment uses:

* **`timeit`** — measures execution time.
* **Node counter** — counts how many nodes each search explores.
* **`py-spy`** — samples Python execution and generates a flamegraph for profiling.

Example py-spy command:

```bash
py-spy record -o sle2_profile.svg -- python search_experiment.py
```

The generated `sle2_profile.svg` provides a visual representation of where execution time was spent during the profiling workload.

---

## Project Structure

```text
Stockholm/
├── index.html
├── style.css
├── script.js
├── inventory_agent.py
├── search_experiment.py
├── AI_Contribution_Log.md
├── README.md
└── .gitignore
```

---

## Running the Inventory Agent

Make sure Python is installed.

```bash
python inventory_agent.py
```

The program uses sample inventory data and prints the agent's decisions.

---

## Running the Search Experiment

Run the BFS vs DFS comparison:

```bash
python search_experiment.py
```

For the dedicated py-spy workload:

```bash
py-spy record -o sle2_profile.svg -- python search_experiment.py
```

---

## SLE-1

The inventory agent was developed as part of the **Self-Learning Exercise (SLE-1)**.

The repository includes an AI Contribution Log documenting:

* AI tools used
* AI-assisted parts
* My own work
* Issues and risks found
* Fixes and limitations
* PEAS description
* Agent type

**AI assistance:** ChatGPT was used during development. GitHub Copilot was not used.

---

## Future Development

The long-term plan is to connect the agent with Stockholm's inventory system and gradually add:

* Real inventory and sales data
* Better inventory decision-making
* Warehouse and product search
* Demand analysis and prediction
* Database integration
* Supplier and order information
* Alerts and purchase recommendations
* More advanced AI-based decision-making

These features are planned and are not all part of the current implementation.

---

## Technology

Currently used:

* HTML
* CSS
* JavaScript
* Python
* Git
* GitHub

---

## Project Status

**Under active development.**

Stockholm currently contains the initial inventory agent and the BFS vs DFS warehouse-search experiment. Further integration between the agent, inventory data, and application is planned.

---

## License

MIT License.
