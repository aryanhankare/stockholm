from warehouse_search import bfs


class InventoryAgent:
    """Rule-based inventory agent for Stockholm.

    The agent observes inventory data, estimates demand, decides what should
    happen, and uses BFS to locate products in the warehouse.
    """

    def __init__(self, low_stock_threshold=10, base_target_stock=25, safety_days=2):
        self.low_stock_threshold = low_stock_threshold
        self.base_target_stock = base_target_stock
        self.safety_days = safety_days
        self.last_cycle = []

        self.warehouse = {
            "Receiving": ["Storage-A", "Storage-B"],
            "Storage-A": ["Receiving", "Rice", "Wheat"],
            "Storage-B": ["Receiving", "Oil", "Sugar"],
            "Rice": ["Storage-A"],
            "Wheat": ["Storage-A"],
            "Oil": ["Storage-B"],
            "Sugar": ["Storage-B"]
        }

    def perceive(self, inventory):
        """Observe the current inventory state."""
        return inventory

    def calculate_sales_velocity(self, sold, days):
        """Calculate average units sold per day."""
        if days <= 0:
            return 0
        return sold / days

    def calculate_target_stock(self, sales_velocity, lead_time):
        """Keep enough stock for supplier lead time plus a safety buffer."""
        coverage_days = max(7, lead_time + self.safety_days)
        demand_stock = int(sales_velocity * coverage_days)
        return max(self.base_target_stock, demand_stock)

    def decide(self, inventory):
        """Analyze inventory and choose a recommended action for each product."""
        decisions = []

        for product in inventory:
            name = product["name"]
            quantity = product["quantity"]
            sold = product["sold"]
            days = product["days"]
            lead_time = product["lead_time"]
            pending_order = product["pending_order"]

            sales_velocity = self.calculate_sales_velocity(sold, days)
            target_stock = self.calculate_target_stock(sales_velocity, lead_time)
            available_after_pending = quantity + pending_order

            if quantity <= 0:
                action = "OUT_OF_STOCK"
                urgency = "HIGH"
            elif available_after_pending < target_stock:
                action = "REORDER"
                if quantity <= self.low_stock_threshold or lead_time >= 7:
                    urgency = "HIGH"
                else:
                    urgency = "MEDIUM"
            else:
                action = "NO_ACTION"
                urgency = "LOW"

            reorder_quantity = max(0, target_stock - available_after_pending)

            decisions.append({
                "product": name,
                "quantity": quantity,
                "sales_velocity": sales_velocity,
                "target_stock": target_stock,
                "lead_time": lead_time,
                "pending_order": pending_order,
                "action": action,
                "urgency": urgency,
                "reorder_quantity": reorder_quantity
            })

        return decisions

    def search_location(self, product_name):
        """Find a product's warehouse path using BFS."""
        name_map = {"Cooking Oil": "Oil"}
        search_name = name_map.get(product_name, product_name)

        return bfs(self.warehouse, "Receiving", search_name)

    def plan_actions(self, decisions):
        """Turn decisions into explicit agent action plans."""
        plans = []

        for decision in decisions:
            path = self.search_location(decision["product"])
            location = " -> ".join(path) if path else "Not found"

            if decision["action"] == "OUT_OF_STOCK":
                next_action = "EMERGENCY_REORDER"
            elif decision["action"] == "REORDER":
                next_action = "PLACE_REORDER"
            else:
                next_action = "MONITOR"

            plan = decision.copy()
            plan["next_action"] = next_action
            plan["location"] = location
            plans.append(plan)

        return plans

    def act(self, plans):
        """Record the planned actions without pretending to place real orders."""
        self.last_cycle = plans
        return plans

    def run(self, inventory):
        """Run one observe -> analyze -> plan -> act cycle."""
        current_state = self.perceive(inventory)
        decisions = self.decide(current_state)
        plans = self.plan_actions(decisions)
        return self.act(plans)


if __name__ == "__main__":
    inventory = [
        {"name": "Rice", "quantity": 10, "sold": 20, "days": 7, "lead_time": 7, "pending_order": 5},
        {"name": "Cooking Oil", "quantity": 25, "sold": 8, "days": 7, "lead_time": 3, "pending_order": 0},
        {"name": "Sugar", "quantity": 0, "sold": 15, "days": 7, "lead_time": 5, "pending_order": 10},
        {"name": "Wheat", "quantity": 12, "sold": 5, "days": 7, "lead_time": 2, "pending_order": 15}
    ]

    agent = InventoryAgent()

    for result in agent.run(inventory):
        print(
            f"{result['product']}: {result['next_action']} | "
            f"Urgency: {result['urgency']} | "
            f"Sales/day: {result['sales_velocity']:.2f} | "
            f"Target: {result['target_stock']} | "
            f"Reorder: {result['reorder_quantity']} | "
            f"Location: {result['location']}"
        )
