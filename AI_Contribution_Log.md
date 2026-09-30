# AI Contribution Log

## Project
Stockholm — Intelligent Inventory Management Agent

## Purpose

This log records the use of AI assistance during development of the Stockholm inventory-agent project.

The current implementation is a rule-based intelligent agent that analyzes inventory information, makes reorder decisions, searches warehouse locations using BFS, and updates the simulated inventory state.

---

## AI Tool Used

- ChatGPT

GitHub Copilot was not used for this project work.

---

## Contribution 1 — Agent Design

### Task

Develop an inventory-management agent using the Perceive → Decide → Act concept.

### AI Assistance

ChatGPT helped explain the agent structure and suggested ways to separate perception, decision-making and action.

### My Contribution

I selected inventory management as the problem, adapted the design to Stockholm and decided which features should actually be implemented.

---

## Contribution 2 — Inventory Decision Logic

The agent was developed to consider:

- current quantity
- units sold
- number of days
- supplier lead time
- pending orders
- base target stock
- safety stock days

The agent calculates sales velocity and uses these values to determine a target stock level and action.

### Current Actions

- `MONITOR`
- `PLACE_REORDER`
- `EMERGENCY_REORDER`

The agent also assigns urgency and calculates the required reorder quantity.

---

## Contribution 3 — Explainable Decisions

The agent generates a reason for each decision. This was added so that the output is not only an action label but also explains why the action was selected.

Example reasoning includes the available quantity, pending order quantity, target stock and sales velocity.

---

## Contribution 4 — Warehouse Search

The Inventory Agent uses BFS from `warehouse_search.py` to locate products in the warehouse graph.

The product location is returned as a path beginning at `Receiving`.

This connects the inventory agent to the BFS work developed during SLE-2.

---

## Contribution 5 — Inventory State Update

The agent can update `pending_order` when a reorder is placed.

It can also simulate receiving pending orders by moving the pending quantity into available stock and clearing the pending order.

This creates a simple inventory cycle without pretending that a real supplier or database is connected.

---

## Testing

The agent was tested with:

- low stock
- zero stock
- sufficient stock with pending orders
- high sales velocity
- different lead times
- different pending-order quantities
- reorder followed by receiving
- warehouse product-location searches

Example test cases included Rice, Cooking Oil, Sugar and Wheat.

---

## Understanding and Ownership

AI-generated suggestions were reviewed and tested before being included.

I selected the project direction, modified and tested the implementation, decided which features to keep, removed unnecessary frontend/invoice material, and verified the architecture and documentation against the actual code.

I understand the purpose and working of the major components of the current agent.

---

## Issues / Risks and Fixes

### Initial design was too broad

The project originally contained frontend and invoice-oriented material that was not useful for the current AI-focused objective.

**Fix:** The unused frontend/invoice files were removed and the project was refocused on the inventory agent.

### Simple rule-based reasoning

The current agent does not learn from data.

**Fix:** This limitation is kept explicit. The rule-based design is being used as a foundation for future improvements.

### Manual/sample inventory data

The current prototype does not use a production database or live business data.

**Fix:** The agent works with structured sample inventory data while the reasoning system is being developed.

---

## PEAS Description

### Performance Measure (P)

- Correctly identify products requiring attention.
- Avoid unnecessary reorder recommendations when available stock plus pending orders is sufficient.
- Calculate a reasonable target stock and reorder quantity.
- Provide an understandable reason for each decision.

### Environment (E)

- Inventory records.
- Product sales information.
- Pending orders.
- Supplier lead times.
- Simulated warehouse graph.

### Actuators (A)

The current agent can:

- recommend `MONITOR`
- recommend `PLACE_REORDER`
- recommend `EMERGENCY_REORDER`
- update pending orders in the simulated inventory state
- simulate receiving pending orders

It does not place real external purchase orders.

### Sensors (S)

The agent reads:

- product name
- current quantity
- units sold
- number of days
- supplier lead time
- pending order quantity

### Agent Type

The current implementation is a **simple rule-based agent**. It perceives inventory information, applies predefined decision rules and performs simulated inventory actions.

Future versions may introduce more advanced demand analysis, learning or optimization after the current reasoning system is understood and tested.
