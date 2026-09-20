from flask import Flask, jsonify, request, send_from_directory
from inventory_agent import InventoryAgent

app = Flask(__name__)

agent = InventoryAgent()

DEFAULT_INVENTORY = [
    {"name": "Rice", "quantity": 10, "sold": 20, "days": 7, "lead_time": 7, "pending_order": 5},
    {"name": "Cooking Oil", "quantity": 25, "sold": 8, "days": 7, "lead_time": 3, "pending_order": 0},
    {"name": "Sugar", "quantity": 0, "sold": 15, "days": 7, "lead_time": 5, "pending_order": 10},
    {"name": "Wheat", "quantity": 12, "sold": 5, "days": 7, "lead_time": 2, "pending_order": 15}
]


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/<path:filename>")
def serve_frontend_file(filename):
    return send_from_directory(".", filename)


@app.route("/api/inventory")
def get_inventory():
    return jsonify(DEFAULT_INVENTORY)


@app.route("/api/agent", methods=["POST"])
def run_agent():
    inventory = request.json or DEFAULT_INVENTORY

    decisions = agent.decide(inventory)

    for decision in decisions:
        path = agent.search_location(decision["product"])

        if path:
            decision["location"] = " -> ".join(path)
        else:
            decision["location"] = "Not found"

    return jsonify(decisions)


if __name__ == "__main__":
    app.run(debug=True)
