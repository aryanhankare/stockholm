from flask import Flask, jsonify, request
from inventory_agent import InventoryAgent
from inventory_store import InventoryStore

app = Flask(__name__)
agent = InventoryAgent()
store = InventoryStore()

DEFAULT_INVENTORY = [
    {"name": "Rice", "quantity": 10, "sold": 20, "days": 7, "lead_time": 7, "pending_order": 5},
    {"name": "Cooking Oil", "quantity": 25, "sold": 8, "days": 7, "lead_time": 3, "pending_order": 0},
    {"name": "Sugar", "quantity": 0, "sold": 15, "days": 7, "lead_time": 5, "pending_order": 10},
    {"name": "Wheat", "quantity": 12, "sold": 5, "days": 7, "lead_time": 2, "pending_order": 15}
]


@app.route("/api/inventory", methods=["GET"])
def get_inventory():
    """Get current inventory from persistent storage."""
    try:
        inventory = store.load_inventory()
        return jsonify(inventory)
    except Exception as e:
        # Fallback to default if storage fails
        return jsonify(DEFAULT_INVENTORY)


@app.route("/api/agent", methods=["POST"])
def run_agent():
    """Run the inventory agent on current inventory, persist result, and record history."""
    # Load current inventory from persistent storage
    inventory = store.load_inventory()

    # Run agent cycle (without receiving orders)
    result = agent.run(inventory, receive_orders=False)

    # Persist updated inventory
    store.save_inventory(result["updated_inventory"])

    # Record in history
    run_id = store.append_run(
        input_inventory=result["input"],
        decisions=result["decisions"],
        plans=result["plans"],
        updated_inventory=result["updated_inventory"],
        received_orders=False
    )

    # Add run_id to response
    result["run_id"] = run_id
    return jsonify(result)


@app.route("/api/history", methods=["GET"])
def get_history():
    """Get recent agent run history."""
    try:
        limit = request.args.get("limit", default=10, type=int)
        limit = max(1, min(limit, 100))  # Clamp between 1 and 100
        runs = store.get_recent_runs(limit)
        return jsonify(runs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/history/<run_id>", methods=["GET"])
def get_history_run(run_id):
    """Get a specific agent run by ID."""
    run = store.get_run(run_id)
    if not run:
        return jsonify({"error": f"Run '{run_id}' not found"}), 404
    return jsonify(run)


if __name__ == "__main__":
    app.run(debug=True)