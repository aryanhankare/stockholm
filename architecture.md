# Stockholm Architecture

Stockholm is an inventory and invoice management system.

## Main Parts

* Web Interface — handles user interaction and invoice UI.
* Flask Backend — connects the web interface with the Python backend.
* Inventory Agent — analyzes inventory data and decides actions.
* Warehouse Search — finds product locations using BFS.
* Invoice Processing — calculates and generates invoice information.

## SLE-3

This document contains the C4 architecture documentation for Stockholm:

1. Context
2. Container
3. Component
4. Code

## C4 Level 1 — Context

### System Context

```text
                    BUSINESS OWNER / USER
                             |
                    uses / interacts with
                             |
                             v
              +-----------------------------+
              |          STOCKHOLM          |
              |                             |
              | Inventory + Invoice         |
              | Management System           |
              +-----------------------------+
```

### Business Owner / User

The business owner or operator uses Stockholm to manage inventory,
generate invoices, search for products, and view inventory decisions.

### External Systems

No external systems are currently required by the implemented Stockholm prototype.

## C4 Level 2 — Container

### Container Diagram

```text
                    BUSINESS OWNER / USER
                             |
                             v
                    +------------------+
                    |  WEB INTERFACE   |
                    |  index.html      |
                    |  script.js       |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    |  FLASK BACKEND   |
                    |     app.py       |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    | INVENTORY AGENT  |
                    | inventory_agent |
                    |     .py          |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    | WAREHOUSE SEARCH |
                    | warehouse_search |
                    |     .py          |
                    +------------------+
```

### Containers

#### 1. Web Interface

**Technology:** HTML, CSS and JavaScript
**Files:** `index.html`, `script.js`

Handles user interaction and displays inventory and invoice-related information.

#### 2. Flask Backend

**Technology:** Python / Flask
**File:** `app.py`

Provides the web server and API endpoints. It receives inventory data,
calls the Inventory Agent, and returns the decisions to the Web Interface.

#### 3. Inventory Agent

**Technology:** Python
**File:** `inventory_agent.py`

Analyzes inventory data and makes inventory decisions based on stock,
sales, lead time and pending orders.

#### 4. Warehouse Search

**Technology:** Python / BFS
**File:** `warehouse_search.py`

Searches the warehouse graph and finds the location/path of a product.

## C4 Level 3 — Component

### Component Diagram

The Inventory Agent is selected as the main container because it contains
the main inventory decision-making logic of Stockholm.

```text
                    INVENTORY AGENT
                    inventory_agent.py
                           |
                           v
                 +-------------------+
                 |    Perception     |
                 |    perceive()     |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 |  Sales Velocity   |
                 | calculate_sales_  |
                 |    velocity()     |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 |  Decision Engine  |
                 |     decide()      |
                 +----+---------+----+
                      |         |
                      |         v
                      |   +-------------------+
                      |   | Warehouse Locator |
                      |   | search_location() |
                      |   +---------+---------+
                      |             |
                      |             v
                      |      warehouse_search
                      |             |
                      |             v
                      |             BFS
                      |
                      v
                 +-------------------+
                 |      Action       |
                 |      act()        |
                 +-------------------+
```

### Components

#### 1. Perception

**Function:** `perceive()`

Receives the current inventory data and provides the state used by the
Inventory Agent.

#### 2. Sales Velocity Calculator

**Function:** `calculate_sales_velocity()`

Calculates the product's sales rate using the number of units sold and
the number of days.

#### 3. Decision Engine

**Function:** `decide()`

Analyzes quantity, sales velocity, lead time and pending orders to determine
the required action, urgency and reorder quantity.

Possible actions include:

* `OUT_OF_STOCK`
* `REORDER`
* `NO_ACTION`

#### 4. Warehouse Locator

**Function:** `search_location()`

Converts product names when required and uses the BFS search from
`warehouse_search.py` to find the product's warehouse path.

#### 5. Action

**Function:** `act()`

Processes the inventory decisions and displays the action, urgency,
sales information, reorder quantity and product location.

## C4 Level 4 — Code

The following code-level elements implement the main Inventory Agent
components:

| Code Element                 | Responsibility                                         |
| ---------------------------- | ------------------------------------------------------ |
| `InventoryAgent`             | Manages inventory analysis and decision-making.        |
| `perceive()`                 | Receives the current inventory state.                  |
| `calculate_sales_velocity()` | Calculates sales rate in units per day.                |
| `decide()`                   | Determines action, urgency and reorder quantity.       |
| `search_location()`          | Finds a product path using BFS.                        |
| `act()`                      | Processes decisions and displays the final result.     |
| `run()`                      | Executes the agent workflow from perception to action. |

## Design Decisions

The system separates the web interface, backend, inventory reasoning and warehouse search
so each part has a clear responsibility. The Inventory Agent is kept as the main reasoning
component because it analyzes inventory data before deciding an action. Warehouse search is
kept as a separate module so BFS can be reused by the Inventory Agent.

## AI Contribution Note

**AI Tool Used:** ChatGPT

**What AI helped with:** Understanding the C4 model, organizing the architecture levels,
and mapping the existing Stockholm code to Context, Container, Component and Code levels.

**What I did myself:** I implemented and tested the project, selected the architecture,
checked the existing files and functions, and verified that the diagrams match the actual
Stockholm implementation.

## Conclusion

The C4 model helped map Stockholm from its overall system context to its main code-level
elements. The architecture clearly separates the web interface, Flask backend, Inventory
Agent and warehouse search. It also shows how the BFS search developed during SLE-2 fits
into the larger Stockholm system.
