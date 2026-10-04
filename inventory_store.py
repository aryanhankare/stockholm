"""
Persistent inventory storage for the Stockholm inventory agent.

Manages data/inventory.json (current state) and data/history.json (agent run history).
"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any


class InventoryStore:
    """Handles persistent storage of inventory and agent run history."""

    MAX_HISTORY_RUNS = 1000

    def __init__(
        self,
        inventory_path: str = "data/inventory.json",
        history_path: str = "data/history.json"
    ):
        self.inventory_path = Path(inventory_path)
        self.history_path = Path(history_path)
        self._ensure_files_exist()

    def _ensure_files_exist(self) -> None:
        """Create default JSON files if they don't exist."""
        # Ensure data directory exists
        self.inventory_path.parent.mkdir(parents=True, exist_ok=True)
        self.history_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.inventory_path.exists():
            default_inventory = {
                "version": 1,
                "updated_at": datetime.utcnow().isoformat() + "Z",
                "products": [
                    {"name": "Rice", "quantity": 10, "sold": 20, "days": 7, "lead_time": 7, "pending_order": 5},
                    {"name": "Cooking Oil", "quantity": 25, "sold": 8, "days": 7, "lead_time": 3, "pending_order": 0},
                    {"name": "Sugar", "quantity": 0, "sold": 15, "days": 7, "lead_time": 5, "pending_order": 10},
                    {"name": "Wheat", "quantity": 12, "sold": 5, "days": 7, "lead_time": 2, "pending_order": 15}
                ]
            }
            self._write_json(self.inventory_path, default_inventory)

        if not self.history_path.exists():
            default_history = {
                "version": 1,
                "runs": []
            }
            self._write_json(self.history_path, default_history)

    def _read_json(self, path: Path) -> dict[str, Any]:
        """Read and parse a JSON file."""
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_json(self, path: Path, data: dict[str, Any]) -> None:
        """Write data to a JSON file with pretty formatting."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _generate_run_id(self) -> str:
        """Generate a unique run ID using UUID."""
        return str(uuid.uuid4())

    def _trim_history(self, history: dict[str, Any]) -> None:
        """Keep only the most recent MAX_HISTORY_RUNS runs."""
        runs = history.get("runs", [])
        if len(runs) > self.MAX_HISTORY_RUNS:
            history["runs"] = runs[-self.MAX_HISTORY_RUNS:]

    # --- Inventory Methods ---

    def load_inventory(self) -> list[dict[str, Any]]:
        """Load the current inventory state."""
        data = self._read_json(self.inventory_path)
        return data.get("products", [])

    def save_inventory(self, products: list[dict[str, Any]]) -> None:
        """Save the current inventory state with updated timestamp."""
        data = {
            "version": 1,
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "products": products
        }
        self._write_json(self.inventory_path, data)

    # --- History Methods ---

    def load_history(self) -> dict[str, Any]:
        """Load the full history object."""
        return self._read_json(self.history_path)

    def save_history(self, history: dict[str, Any]) -> None:
        """Save the full history object."""
        self._write_json(self.history_path, history)

    def append_run(
        self,
        input_inventory: list[dict[str, Any]],
        decisions: list[dict[str, Any]],
        plans: list[dict[str, Any]],
        updated_inventory: list[dict[str, Any]],
        received_orders: bool = False
    ) -> str:
        """Append a new agent run to history. Returns the run_id."""
        history = self.load_history()
        run_id = self._generate_run_id()

        run_data = {
            "run_id": run_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "input_inventory": input_inventory,
            "decisions": decisions,
            "plans": plans,
            "updated_inventory": updated_inventory,
            "received_orders": received_orders
        }

        history["runs"].append(run_data)
        self._trim_history(history)
        self.save_history(history)
        return run_id

    def get_run(self, run_id: str) -> dict[str, Any] | None:
        """Get a specific run by run_id."""
        history = self.load_history()
        for run in history.get("runs", []):
            if run.get("run_id") == run_id:
                return run
        return None

    def get_recent_runs(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get the most recent runs, newest first."""
        history = self.load_history()
        runs = history.get("runs", [])
        return runs[-limit:][::-1]  # Reverse to get newest first