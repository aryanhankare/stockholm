# SLE-3 — C4 Architecture Report

**Project:** Stockholm — Intelligent Inventory Management Agent  
**Student:** Aaryan Hankare  
**PRN:** 25UAM019  
**Division:** A  
**Subject:** 02AML204 — Introduction to Artificial Intelligence

## 1. Aim

To document the Stockholm inventory agent using the C4 architecture model and describe the system from context level to code level.

## 2. Project Overview

Stockholm is a learning project focused on an intelligent inventory management agent. The current implementation is centered on the Python Inventory Agent and the warehouse search it uses.

The agent analyzes inventory state using quantity, sales history, sales velocity, lead time, pending orders and target stock. It produces actions such as `MONITOR`, `PLACE_REORDER` and `EMERGENCY_REORDER`, along with urgency, reorder quantity and a reason. It can also simulate receiving pending orders.

## 3. C4 Level 1 — Context

**Business User / Operator → Stockholm → Inventory decisions and order updates**

The user supplies or manages inventory information and uses the agent output to understand which products need attention.

No external production systems are currently required by the implemented prototype.

**Diagram to insert in final report:** Context diagram showing the Business User / Operator and Stockholm.

## 4. C4 Level 2 — Container

The current runtime architecture contains three main containers/modules:

| Container | File | Responsibility |
|---|---|---|
| Flask API | `app.py` | Provides API endpoints for inventory data and agent execution. |
| Inventory Agent | `inventory_agent.py` | Performs inventory reasoning, planning and state updates. |
| Warehouse Search | `warehouse_search.py` | Provides BFS-based product location search. |

`search_experiment.py` is a separate SLE-2 experiment and is not a separate runtime container of the Inventory Agent.

**Diagram to insert in final report:** Container diagram showing Flask API → Inventory Agent → Warehouse Search / BFS.

## 5. C4 Level 3 — Component

The Inventory Agent is selected for the component-level view because it contains the main intelligent decision-making logic.

### Components

1. **Perception — `perceive()`**
   - Receives the current inventory state.

2. **Sales Velocity Calculator — `calculate_sales_velocity()`**
   - Calculates units sold per day.

3. **Decision Engine — `decide()`**
   - Determines action, urgency, target stock, reorder quantity and reason.

4. **Action Planner — `plan_actions()`**
   - Converts decisions into simple executable plans.

5. **Warehouse Locator — `search_location()`**
   - Calls BFS from `warehouse_search.py` to locate a product from `Receiving`.

6. **Action / State Update — `act()`**
   - Updates pending orders when a reorder is placed.

7. **Order Receiving — `receive_orders()`**
   - Simulates delivery by moving pending orders into available stock.

8. **Agent Cycle — `run()`**
   - Coordinates the inventory-agent cycle.

**Diagram to insert in final report:** InventoryAgent component diagram showing the flow from perception through decision and action/receiving, with warehouse location handled through BFS.

## 6. C4 Level 4 — Code

| Code Element | Responsibility |
|---|---|
| `InventoryAgent` | Main class containing inventory-agent logic. |
| `__init__()` | Sets thresholds, safety-stock settings and warehouse graph. |
| `perceive()` | Receives current inventory state. |
| `calculate_sales_velocity()` | Calculates units sold per day. |
| `decide()` | Determines action, urgency, target stock, reorder quantity and reason. |
| `plan_actions()` | Creates an action plan from decisions. |
| `search_location()` | Finds product location using BFS. |
| `act()` | Updates pending orders for reorder decisions. |
| `receive_orders()` | Converts pending orders into available stock. |
| `run()` | Executes the complete agent cycle. |

## 7. Working Evidence

The final report should include screenshots of the actual terminal output at these locations:

### Screenshot 1 — Agent Decision Cycle

Show `python inventory_agent.py` output containing:
- Rice: `PLACE_REORDER`
- Sugar: `EMERGENCY_REORDER`
- Cooking Oil and Wheat: `MONITOR`
- BFS warehouse locations
- Decision reasons

### Screenshot 2 — After Reorder

Show the `AFTER REORDER` inventory state where reorder quantities have been added to `pending_order`.

### Screenshot 3 — After Delivery

Show the `AFTER DELIVERY` inventory state where pending orders become available quantity and `pending_order` becomes zero.

## 8. SLE-2 Connection

SLE-2 compared BFS and DFS for warehouse search. In the current Stockholm implementation, `InventoryAgent.search_location()` uses BFS from `warehouse_search.py` to locate products. This connects the earlier search experiment to the current inventory-agent architecture.

## 9. Design Decisions

1. The Inventory Agent is the core of Stockholm.
2. Warehouse search is separated from the agent so BFS has a clear responsibility.
3. The current agent is rule-based, making decisions transparent and testable while providing a foundation for future AI improvements.
4. The architecture represents implemented code rather than planned features.
5. Order receiving is simulated in memory; there is currently no real supplier or database integration.

## 10. AI Contribution Note

**AI Tool Used:** ChatGPT

AI assistance was used to understand and organize the C4 architecture, review code structure, improve documentation and assist with development and debugging.

The student selected the project direction, implemented and tested the code, made final architecture decisions and verified the documentation against the actual repository.

## 11. Conclusion

The C4 model maps Stockholm from overall system context to the code-level functions of the Inventory Agent. The architecture keeps the project focused on inventory intelligence while retaining the BFS warehouse search developed during SLE-2. It provides a foundation for gradually adding more advanced inventory reasoning as the project develops.
