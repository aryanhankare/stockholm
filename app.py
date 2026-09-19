from flask import Flask, jsonify, request, send_from_directory
from inventory_agent import InventoryAgent

app = Flask(__name__)

agent = InventoryAgent()


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/api/agent", methods=["POST"])
def run_agent():

    inventory = request.json

    decisions = agent.decide(inventory)

    for decision in decisions:

        path = agent.search_location(
            decision["product"]
        )

        if path:
            decision["location"] = " -> ".join(path)
        else:
            decision["location"] = "Not found"

    return jsonify(decisions)


if __name__ == "__main__":
    app.run(debug=True)