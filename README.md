# Stockholm

Stockholm is an inventory and invoice management project being built as a learning project.

## Current Project

The repository currently contains:

- Invoice generator frontend
- Inventory management prototype
- A simple rule-based inventory agent
- AI Contribution Log for SLE-1

The inventory agent follows a basic:

**Perceive → Decide → Act**

cycle.

It currently checks product quantities and produces one of three decisions:

- `OUT_OF_STOCK` — quantity is 0 or below
- `REORDER` — quantity is at or below the low-stock threshold
- `NO_ACTION` — stock is above the threshold

The agent is currently a Python prototype and is not yet connected to the web application or a database.

## Project Structure

```
Stockholm/
├── index.html
├── style.css
├── script.js
├── inventory_agent.py
├── AI_Contribution_Log.md
├── README.md
└── .gitignore
```

## Running the Inventory Agent

Make sure Python is installed, then run:

```bash
python inventory_agent.py
```

The program uses sample inventory data and prints the agent's decisions.

## SLE-1

The inventory agent was created as part of the Self-Learning Exercise (SLE-1).

The repository includes an AI Contribution Log documenting:

- AI tools used
- AI-assisted parts
- My own work
- Issues and risks found
- Fixes and limitations
- PEAS description and agent type

Only ChatGPT was used for AI assistance in this work. GitHub Copilot was not used.

## Future Development

The long-term plan is to connect the agent with Stockholm's inventory system and gradually add:

- Real inventory and sales data
- Better decision-making rules
- Search and optimization
- Demand analysis and prediction
- Database integration
- More useful actions such as alerts and purchase recommendations

These features are planned and are not part of the current implementation.

## Technology

Currently used:

- HTML
- CSS
- JavaScript
- Python
- Git & GitHub

More technologies may be added as the project develops.

## Project Status

Under active development.

## License

MIT License.
