from warehouse_search import bfs


class InventoryAgent:

    def __init__(self, low_stock_threshold=10, base_target_stock=25):
        self.low_stock_threshold = low_stock_threshold
        self.base_target_stock = base_target_stock

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
        return inventory

    def calculate_sales_velocity(self, sold, days):
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

            demand_stock = int(sales_velocity * 7)

            target_stock = max(
                self.base_target_stock,
                demand_stock
            )

            available_after_pending = (
                quantity + pending_order
            )

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

            reorder_quantity = max(
                0,
                target_stock - available_after_pending
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
                "reorder_quantity": reorder_quantity
            })

        return actions

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
            lead_time = decision["lead_time"]
            pending_order = decision["pending_order"]
            reorder_quantity = decision["reorder_quantity"]

            path = self.search_location(product)

            if path:
                location = " -> ".join(path)
            else:
                location = "Not found"

            print(
                f"{product}: {action} | "
                f"Urgency: {urgency} | "
                f"Sales/day: {velocity:.2f} | "
                f"Lead time: {lead_time} days | "
                f"Pending: {pending_order} units | "
                f"Reorder: {reorder_quantity} units | "
                f"Location: {location}"
            )

    def run(self, inventory):

        current_state = self.perceive(inventory)

        decisions = self.decide(current_state)

        self.act(decisions)


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
        base_target_stock=25
    )

    agent.run(inventory)