class InventoryAgent:

    def __init__(self, low_stock_threshold=10):
        self.low_stock_threshold = low_stock_threshold

    def perceive(self, inventory):
        return inventory

    def decide(self, inventory):
        actions = []

        for product in inventory:
            name = product["name"]
            quantity = product["quantity"]

            if quantity <= 0:
                actions.append({
                    "product": name,
                    "action": "OUT_OF_STOCK"
                })

            elif quantity <= self.low_stock_threshold:
                actions.append({
                    "product": name,
                    "action": "REORDER"
                })

            else:
                actions.append({
                    "product": name,
                    "action": "NO_ACTION"
                })

        return actions

    def act(self, decisions):
        for decision in decisions:
            print(
                f"{decision['product']}: "
                f"{decision['action']}"
            )

    def run(self, inventory):
        current_state = self.perceive(inventory)
        decisions = self.decide(current_state)
        self.act(decisions)


if __name__ == "__main__":

    inventory = [
        {"name": "Rice", "quantity": 10},
        {"name": "Cooking Oil", "quantity": 25},
        {"name": "Sugar", "quantity": 0},
        {"name": "Wheat", "quantity": 12}
    ]

    agent = InventoryAgent(low_stock_threshold=10)

    agent.run(inventory)