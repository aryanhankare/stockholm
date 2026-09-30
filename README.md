# Stockholm

Stockholm is a learning project focused on building an intelligent inventory management agent.

The current project is intentionally small: the main focus is the Python inventory agent and the warehouse search it uses.

## Current Focus

The `InventoryAgent` follows a simple **Perceive → Decide → Act** cycle.

It currently:

- reads inventory state
- calculates sales velocity
- estimates target stock using demand, lead time and safety stock
- considers pending orders
- decides whether to monitor, place a reorder, or perform an emergency reorder
- assigns urgency to the decision
- calculates the required reorder quantity
- explains the reason for its decision
- locates products in a warehouse graph using BFS
- updates pending orders after a reorder decision
- can simulate receiving pending orders

The current agent is rule-based. It is designed as a foundation that can become more advanced as the project develops.

## Agent Decision Flow

```text
Inventory State
      |
      v
  Perception
      |
      v
Sales Velocity
      |
      v
Decision Engine
      |
      +----> MONITOR
      |
      +----> PLACE_REORDER
      |
      +----> EMERGENCY_REORDER
      |
      v
Warehouse Location
      |
      v
Action / Order Update
      |
      v
Receive Orders
```

## Main Files

```text
Stockholm/
├── inventory_agent.py      # Main inventory agent
├── warehouse_search.py     # BFS warehouse search used by the agent
├── app.py                  # Small Flask API entry point
├── search_experiment.py    # SLE-2 BFS vs DFS experiment
├── architecture.md         # SLE-3 C4 architecture
├── sle2.md                 # SLE-2 documentation
├── AI_Contribution_Log.md  # AI-assisted development record
└── README.md
```

## Running the Agent

Make sure Python is installed, then run:

```bash
python inventory_agent.py
```

The program uses sample inventory data and prints the agent's decisions, reasons, warehouse locations and inventory state after the reorder/receiving cycle.

## Example Decisions

For the included sample data, the agent can produce decisions such as:

- `PLACE_REORDER` — additional stock is required after considering pending orders.
- `EMERGENCY_REORDER` — the product is currently out of stock.
- `MONITOR` — available stock including pending orders is sufficient for the current target.

## Warehouse Search

The agent uses Breadth-First Search (BFS) from `warehouse_search.py` to find a product's path from `Receiving` through the warehouse graph.

The BFS vs DFS comparison was developed separately as SLE-2 and is documented in `sle2.md`.

## SLE Work

### SLE-1

The project includes an AI Contribution Log documenting the use of ChatGPT during development, the student's contribution, testing, limitations and the PEAS description of the agent.

### SLE-2

SLE-2 compares BFS and DFS on a warehouse graph using execution time and nodes explored, with additional profiling using `py-spy`.

### SLE-3

SLE-3 documents Stockholm using the C4 architecture model:

1. Context
2. Container
3. Component
4. Code

## Current Limitations

The current prototype uses sample/manual inventory data and rule-based decisions. It does not use a production database, machine-learning demand prediction, real supplier integration or autonomous external purchasing.

These are future development possibilities, not current features.

## Future Direction

The project will be developed gradually as my understanding of AI and intelligent agents improves. Possible future work includes better demand analysis, richer inventory state, supplier information, improved search/optimization and more capable decision-making.

## Technology

- Python
- Flask
- Git
- GitHub

## Project Status

**Under active development.**

The current priority is improving and documenting the inventory agent rather than building a separate invoice or frontend application.

## License

MIT License.
