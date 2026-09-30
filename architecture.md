# Stockholm Architecture

Stockholm is a learning project focused on an intelligent inventory management agent.

The current implementation is intentionally centered on the Python Inventory Agent and the warehouse search it uses.

## Main Parts

- **Inventory Agent** — analyzes inventory state and makes inventory decisions.
- **Warehouse Search** — finds product locations using BFS.
- **Flask API** — provides a small programmatic entry point for inventory data and agent execution.
- **SLE-2 Search Experiment** — compares BFS and DFS on a separate warehouse-search workload.

The previously used invoice/frontend files are no longer part of the current project architecture.

## SLE-3 — C4 Architecture

This document describes Stockholm at four levels:

1. Context
2. Container
3. Component
4. Code

---

# C4 Level 1 — Context

```text
                  BUSINESS USER / OPERATOR
                           |
                           | inventory data / requests
                           v
                +--------------------------+
                |        STOCKHOLM         |
                |                          |
                |  Inventory Agent         |
                |  + Warehouse Search      |
                +--------------------------+
                           |
                           v
                    Inventory decisions
                    and order updates
```

### Business User / Operator

The user supplies or manages inventory information and uses the agent's output to understand which products need attention.

### External Systems

No external production systems are currently required by the implemented prototype.

---

# C4 Level 2 — Container

```text
                 BUSINESS USER / OPERATOR
                           |
                           v
                 +--------------------+
                 |    Flask API       |
                 |      app.py        |
                 +---------+----------+
                           |
                           v
                 +--------------------+
                 |   Inventory Agent  |
                 | inventory_agent.py  |
                 +---------+----------+
                           |
                           v
                 +--------------------+
                 |  Warehouse Search  |
                 | warehouse_search.py|
                 +--------------------+
                           |
                           v
                          BFS
```

### 1. Flask API

**Technology:** Python / Flask

**File:** `app.py`

Provides a small API entry point for inventory data and agent execution. It creates an `InventoryAgent` and calls the agent's decision logic.

### 2. Inventory Agent

**Technology:** Python

**File:** `inventory_agent.py`

This is the main reasoning container. It perceives inventory state, calculates sales velocity, determines target stock, selects an action and urgency, plans the action, updates pending orders and can simulate receiving those orders.

### 3. Warehouse Search

**Technology:** Python / BFS

**File:** `warehouse_search.py`

Contains the BFS implementation used by the Inventory Agent to locate products in the warehouse graph.

### SLE-2 Search Experiment

`search_experiment.py` is a separate project experiment used for SLE-2. It contains its own BFS and DFS implementations and measures execution time and nodes explored on a larger test warehouse graph. It is not a separate runtime container of the Inventory Agent.

---

# C4 Level 3 — Component

The Inventory Agent is selected for the component-level view because it contains the main intelligent decision-making logic.

```text
                 INVENTORY AGENT
                       |
                       v
                +-------------+
                |  Perception |
                |  perceive()  |
                +------+------+ 
                       |
                       v
             +---------------------+
             | Sales Velocity       |
             | calculate_sales_     |
             | velocity()           |
             +----------+----------+
                        |
                        v
                +---------------+
                | Decision      |
                | Engine        |
                | decide()      |
                +-------+-------+
                        |
              +---------+---------+
              |                   |
              v                   v
       +-------------+     +-------------+
       | Plan Action |     | Warehouse   |
       | plan_actions|     | Locator     |
       +------+------+     | search_     |
              |            | location()  |
              |            +------+------+ 
              |                   |
              |                   v
              |                  BFS
              v
       +-------------+
       | Action      |
       | act()       |
       +------+------+ 
              |
              v
       +-------------+
       | Receiving   |
       | receive_    |
       | orders()    |
       +-------------+
```

## Components

### 1. Perception — `perceive()`

Receives the current inventory state used by the agent.

### 2. Sales Velocity Calculator — `calculate_sales_velocity()`

Calculates sales per day from units sold and the number of days. It also avoids division by zero when the supplied number of days is zero or negative.

### 3. Decision Engine — `decide()`

Uses quantity, sales velocity, lead time, pending orders, base target stock and safety stock to determine:

- action
- urgency
- target stock
- reorder quantity
- reason for the decision

Current actions are:

- `MONITOR`
- `PLACE_REORDER`
- `EMERGENCY_REORDER`

### 4. Action Planner — `plan_actions()`

Converts a decision into a simple plan, such as placing an order for the calculated quantity or continuing to monitor inventory.

### 5. Warehouse Locator — `search_location()`

Maps product names when necessary and calls BFS from `warehouse_search.py` to find the product's path from `Receiving`.

### 6. Action / State Update — `act()`

Updates `pending_order` when the agent decides to place a reorder.

### 7. Order Receiving — `receive_orders()`

Simulates delivery by moving pending orders into available quantity and clearing the pending order.

### 8. Agent Cycle — `run()`

Coordinates perception, decision-making, planning, action, optional receiving, location lookup and output.

---

# C4 Level 4 — Code

| Code Element | Responsibility |
|---|---|
| `InventoryAgent` | Main class containing the inventory-agent logic. |
| `__init__()` | Sets thresholds, safety-stock settings and warehouse graph. |
| `perceive()` | Receives the current inventory state. |
| `calculate_sales_velocity()` | Calculates units sold per day. |
| `decide()` | Determines action, urgency, target stock, reorder quantity and reason. |
| `plan_actions()` | Creates a simple action plan from decisions. |
| `search_location()` | Finds a product location using BFS. |
| `act()` | Updates pending orders for reorder decisions. |
| `receive_orders()` | Converts pending orders into available stock. |
| `run()` | Executes the complete agent cycle. |

---

# Design Decisions

1. **The Inventory Agent is the core of Stockholm.** The project is currently focused on intelligent inventory reasoning rather than a separate invoice or frontend application.
2. **Warehouse search is separated from the agent.** BFS is kept in `warehouse_search.py` so the search logic has a clear responsibility.
3. **The agent is rule-based.** This makes the current decisions transparent and easy to test while providing a foundation for future AI work.
4. **The architecture reflects the implemented code.** Features that are not currently implemented are not represented as active system components.
5. **Order receiving is simulated.** The current implementation updates in-memory inventory data; it does not connect to a real supplier or database.

# AI Contribution Note

**AI Tool Used:** ChatGPT

AI assistance was used to understand and organize the C4 architecture, review code structure, improve documentation and assist with development/debugging.

The student selected the project direction, implemented and tested the code, made the final architecture decisions and verified the documentation against the actual repository.

# Conclusion

The C4 model maps Stockholm from its overall context to the code-level functions of the Inventory Agent. The architecture keeps the project focused on inventory intelligence while retaining the BFS warehouse search developed during SLE-2. It provides a clean foundation for gradually adding more advanced inventory reasoning as the project develops.
