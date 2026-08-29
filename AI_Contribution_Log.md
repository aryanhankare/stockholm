# AI Contribution Log

## Project
Stockholm – Invoice and Inventory Management System

## SLE-1: AI-Augmented Workflow

### Objective

A basic rule-based inventory management agent was developed
as part of the Stockholm project.

The agent observes inventory quantities and decides whether
each product requires reordering, no action, or is out of stock.

---

## AI Tools Used

- ChatGPT
- GitHub Copilot (if used)

---

## Contribution 1 – Agent Design

### Task
Develop a basic intelligent agent for Stockholm's inventory
management system.

### AI Assistance
AI was used to suggest a basic rule-based agent structure
using the Perceive → Decide → Act cycle.

### My Contribution
I selected inventory management as the use case and adapted
the agent to work with product names and quantities.

---

## Contribution 2 – Decision Logic

### Task
Create decision rules for inventory levels.

### AI Assistance
AI suggested conditional logic for identifying low-stock
and out-of-stock products.

### My Contribution
I selected the low-stock threshold and tested the behaviour
using different inventory quantities.

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

The AI-generated suggestions were reviewed and tested before
being included in the project.

The developer understands the purpose and working of each
major component of the agent and made changes according to
the requirements of the Stockholm project.

---

## Current Limitations

The current agent uses manually provided inventory data and
rule-based decision making.

It is currently a prototype and is not directly connected
to a production database.

Future versions can connect the agent to Stockholm's inventory
data and generate actual reorder recommendations.
