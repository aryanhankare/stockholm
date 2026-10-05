from copy import deepcopy

from flask import Flask, jsonify, request
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
    return """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Stockholm | Inventory Agent</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; background: #f4f6f8; color: #17202a; }
        main { max-width: 1050px; margin: 40px auto; padding: 0 20px; }
        h1 { margin-bottom: 6px; }
        .subtitle { color: #5f6b76; margin-top: 0; }
        .card { background: white; border: 1px solid #dfe4e8; border-radius: 10px; padding: 20px; margin-top: 20px; }
        button { border: 0; border-radius: 7px; padding: 10px 15px; margin-right: 8px; cursor: pointer; }
        .primary { background: #17202a; color: white; }
        .secondary { background: #e8edf1; color: #17202a; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { text-align: left; padding: 10px; border-bottom: 1px solid #e5e8eb; }
        th { background: #f7f8f9; }
        #status { margin-top: 14px; color: #5f6b76; }
        .error { color: #b42318; }
    </style>
</head>
<body>
<main>
    <h1>Stockholm</h1>
    <p class="subtitle">Inventory Agent demonstration</p>

    <div class="card">
        <h2>Agent Controls</h2>
        <p>Run the same inventory decision cycle used by the Python Inventory Agent.</p>
        <button class="primary" onclick="runAgent(false)">Run Agent</button>
        <button class="secondary" onclick="runAgent(true)">Run + Receive Orders</button>
        <div id="status">Ready.</div>
    </div>

    <div class="card">
        <h2>Inventory Decisions</h2>
        <div id="results">Run the agent to see its decisions.</div>
    </div>
</main>

<script>
async function runAgent(receiveOrders) {
    const status = document.getElementById("status");
    const results = document.getElementById("results");

    status.textContent = "Running agent...";
    status.className = "";

    try {
        const response = await fetch("/api/agent", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({receive_orders: receiveOrders})
        });

        if (!response.ok) {
            throw new Error("Agent request failed (" + response.status + ")");
        }

        const data = await response.json();
        const rows = data.decisions.map(function(d) {
            return "<tr>" +
                "<td>" + d.product + "</td>" +
                "<td>" + d.quantity + "</td>" +
                "<td>" + d.sales_velocity.toFixed(2) + "</td>" +
                "<td>" + d.target_stock + "</td>" +
                "<td>" + d.action + "</td>" +
                "<td>" + d.urgency + "</td>" +
                "<td>" + d.reorder_quantity + "</td>" +
                "</tr>";
        }).join("");

        results.innerHTML =
            "<table>" +
            "<thead><tr>" +
            "<th>Product</th><th>Stock</th><th>Sales/day</th>" +
            "<th>Target</th><th>Action</th><th>Urgency</th><th>Reorder</th>" +
            "</tr></thead>" +
            "<tbody>" + rows + "</tbody>" +
            "</table>";

        status.textContent = receiveOrders
            ? "Agent cycle completed and pending orders were received."
            : "Agent cycle completed.";
    } catch (error) {
        status.textContent = error.message;
        status.className = "error";
    }
}
</script>
</body>
</html>
"""


@app.route("/api/inventory")
def get_inventory():
    return jsonify(deepcopy(DEFAULT_INVENTORY))


@app.route("/api/agent", methods=["POST"])
def run_agent():
    payload = request.get_json(silent=True) or {}
    inventory = deepcopy(payload.get("inventory", DEFAULT_INVENTORY))
    receive_orders = bool(payload.get("receive_orders", False))

    return jsonify(
        agent.run(
            inventory,
            receive_orders=receive_orders
        )
    )


if __name__ == "__main__":
    app.run(debug=True)
