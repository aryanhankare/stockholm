# AI Contribution Log

## Project
Stockholm – Invoice and Inventory Management System

## SLE-1: AI-Augmented Workflow

### Objective
A basic rule-based inventory management agent was developed as part of the Stockholm project.

The agent observes inventory quantities and decides whether each product requires reordering, no action, or is out of stock.

---

## AI Tools Used

- ChatGPT

GitHub Copilot was not used for this work.

---

## Contribution 1 – Agent Design

### Task
Develop a basic intelligent agent for Stockholm's inventory management system.

### AI Assistance
ChatGPT was used to suggest a basic rule-based agent structure using the Perceive → Decide → Act cycle.

### My Contribution
I selected inventory management as the use case and adapted the agent to work with product names and quantities.

---

## Contribution 2 – Decision Logic

### Task
Create decision rules for inventory levels.

### AI Assistance
ChatGPT suggested conditional logic for identifying low-stock and out-of-stock products.

### My Contribution
I selected the low-stock threshold and tested the behaviour using different inventory quantities.

---

## Testing

The agent was tested using:

- Products below the threshold
- Products equal to the threshold
- Products above the threshold
- Products with zero quantity
- Multiple products simultaneously

### Test Results

| Product | Quantity | Expected Action | Result |
|---|---:|---|---|
| Rice | 5 | REORDER | PASS |
| Rice | 10 | REORDER | PASS |
| Rice | 15 | NO_ACTION | PASS |
| Sugar | 0 | OUT_OF_STOCK | PASS |

---

## Understanding and Ownership

ChatGPT-generated suggestions were reviewed and tested before being included in the project.

I selected the Stockholm inventory use case, set the decision threshold, adapted the code, ran the tests, and reviewed the resulting behaviour.

I understand the purpose and working of the major components of the current agent.

---

## Issues / Risks Found and Fixes

- The initial AI-assisted design was a simple rule-based prototype rather than a complete autonomous inventory system. This limitation was identified and documented.
- The current agent depends on manually supplied inventory data. This was kept intentionally as the first prototype and is planned for later integration with Stockholm's application data.

---

## Current Limitations

The current agent uses manually provided inventory data and rule-based decision making.

It is currently a prototype and is not directly connected to a production database.

It does not yet use sales history, demand prediction, supplier lead time, learning, or autonomous actions.

---

## PEAS Description

The Stockholm Inventory Agent can be described using the PEAS framework.

### Performance Measure (P)
- Correctly identify out-of-stock products.
- Correctly identify products requiring reorder.
- Avoid unnecessary reorder recommendations.

### Environment (E)
- Stockholm's inventory management environment.
- Products and their available quantities.

### Actuators (A)
- Currently outputs the recommended action:
  - REORDER
  - NO_ACTION
  - OUT_OF_STOCK

### Sensors (S)
- Product information.
- Current inventory quantity.

### Agent Type

The implemented agent is a simple rule-based agent. It perceives inventory information, applies predefined decision rules, and produces an appropriate action recommendation.

Future versions can connect the agent to Stockholm's inventory data and progressively add more informed decision-making and real actions.
