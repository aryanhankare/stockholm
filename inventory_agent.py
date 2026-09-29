from warehouse_search import bfs


class InventoryAgent:

    def __init__(
        self,
        low_stock_threshold=10,
        base_target_stock=25,
        safety_stock_days=2
    ):
        self.low_stock_threshold = low_stock_threshold
        self.base_target_stock = base_target_stock
        self.safety_stock_days = safety_stock_days

        self.warehouse = {
            "Receiving": ["Storage-A", "Storage-B"],
            "Storage-A": ["Receiving", "Rice", "Wheat"],
            "Storage-B": ["Receiving", "Oil", "Sugar"],
            "Rice": ["Storage-A"],
            "Wheat": ["Storage-A"],
            "Oil": ["Storage-B"],
            "Sugar": ["Storage-B"]
        }

        self.last_cycle = None

    def perceive(self, inventory):
        return inventory

    def calculate_sales_velocity(self, sold, days):
        if days <= 0:
            return 0

        return sold / days

    def decide(self, inventory):
        actions = []

        for product in inventory:

            name = product["name"]
            quantity = product["quantity"]
            sold = product["sold"]
            days = product["days"]
            lead_time = product["lead_time"]
            pending_order = product["pending_order"]

            sales_velocity = self.calculate_sales_velocity(
                sold,
                days
            )

            demand_stock = int(
                sales_velocity * (lead_time + self.safety_stock_days)
            )

            target_stock = max(
                self.base_target_stock,
                demand_stock
            )

            available_after_pending = (
                quantity + pending_order
            )

            if quantity <= 0:

                action = "EMERGENCY_REORDER"
                urgency = "HIGH"

            elif available_after_pending < target_stock:

                action = "PLACE_REORDER"

                if (
                    quantity <= self.low_stock_threshold
                    or lead_time >= 7
                ):
                    urgency = "HIGH"
                else:
                    urgency = "MEDIUM"

            else:

                action = "MONITOR"
                urgency = "LOW"

            reorder_quantity = max(
                0,
                target_stock - available_after_pending
            )

            if action == "EMERGENCY_REORDER":

                reason = (
                    f"{name} is out of stock. "
                    f"Sales velocity is "
                    f"{sales_velocity:.2f} units/day."
                )

            elif action == "PLACE_REORDER":

                reason = (
                    f"{name} has {quantity} units available "
                    f"and {pending_order} units pending. "
                    f"Target stock is {target_stock}, "
                    f"so {reorder_quantity} more units are needed."
                )

            else:

                reason = (
                    f"{name} has enough stock considering "
                    f"pending orders. Available after pending "
                    f"order: {available_after_pending} units, "
                    f"target: {target_stock}."
                )

            actions.append({
                "product": name,
                "quantity": quantity,
                "sales_velocity": sales_velocity,
                "target_stock": target_stock,
                "lead_time": lead_time,
                "pending_order": pending_order,
                "action": action,
                "urgency": urgency,
                "reorder_quantity": reorder_quantity,
                "reason": reason
            })

        return actions

    def plan_actions(self, decisions):

        plans = []

        for decision in decisions:

            if decision["action"] == "EMERGENCY_REORDER":

                plan = "Create emergency reorder immediately."

            elif decision["action"] == "PLACE_REORDER":

                plan = (
                    f"Prepare reorder for "
                    f"{decision['reorder_quantity']} units."
                )

            else:

                plan = "Continue monitoring inventory."

            plans.append({
                "product": decision["product"],
                "action": decision["action"],
                "urgency": decision["urgency"],
                "reorder_quantity": decision["reorder_quantity"],
                "plan": plan,
                "reason": decision["reason"]
            })

        return plans

    def search_location(self, product_name):

        name_map = {
            "Cooking Oil": "Oil"
        }

        search_name = name_map.get(
            product_name,
            product_name
        )

        path = bfs(
            self.warehouse,
            "Receiving",
            search_name
        )

        return path

    def act(self, decisions):

        for decision in decisions:

            product = decision["product"]
            action = decision["action"]
            urgency = decision["urgency"]
            velocity = decision["sales_velocity"]
            target_stock = decision["target_stock"]
            reorder_quantity = decision["reorder_quantity"]

            path = self.search_location(product)

            if path:
                location = " -> ".join(path)
            else:
                location = "Not found"

            output = (
                f"{product}: {action} | "
                f"Urgency: {urgency} | "
                f"Sales/day: {velocity:.2f} | "
                f"Target: {target_stock} | "
                f"Reorder: {reorder_quantity} | "
                f"Location: {location}"
            )

            print(output)
            print(f"Reason: {decision['reason']}")
            print()

    def run(self, inventory):

        current_state = self.perceive(inventory)

        decisions = self.decide(current_state)

        plans = self.plan_actions(decisions)

        self.last_cycle = {
            "input": current_state,
            "decisions": decisions,
            "plans": plans
        }

        self.act(decisions)

        return self.last_cycle


if __name__ == "__main__":

    inventory = [
        {
            "name": "Rice",
            "quantity": 10,
            "sold": 20,
            "days": 7,
            "lead_time": 7,
            "pending_order": 5
        },
        {
            "name": "Cooking Oil",
            "quantity": 25,
            "sold": 8,
            "days": 7,
            "lead_time": 3,
            "pending_order": 0
        },
        {
            "name": "Sugar",
            "quantity": 0,
            "sold": 15,
            "days": 7,
            "lead_time": 5,
            "pending_order": 10
        },
        {
            "name": "Wheat",
            "quantity": 12,
            "sold": 5,
            "days": 7,
            "lead_time": 2,
            "pending_order": 15
        }
    ]

    agent = InventoryAgent(
        low_stock_threshold=10,
        base_target_stock=25,
        safety_stock_days=2
    )

    agent.run(inventory)