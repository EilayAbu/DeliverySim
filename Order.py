from datetime import datetime
import random
import json
import os

# === מזהה ייחודי בן 6 ספרות ===
def load_existing_order_ids(filename="orders.json"):
    ids = set()
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                data = json.load(f)
                for entry in data:
                    ids.add(entry["order_id"])
            except json.JSONDecodeError:
                pass
    return ids

existing_order_ids = load_existing_order_ids()

def generate_unique_order_id():
    while True:
        order_id = random.randint(100000, 999999)
        if order_id not in existing_order_ids:
            existing_order_ids.add(order_id)
            return order_id

class Order:
    def __init__(self, order_id, customer_id, destination, customer_name=None, pickup_address=None, item_description=None):
        self.order_id = order_id
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.pickup_address = pickup_address
        self.item_description = item_description
        self.destination = destination
        self.status = 'pending'
        self.date = datetime.now()
        self.courier = None
        self.courier_id = None  # ← להשלמה עם json

    def get_order_id(self) -> int:
        return self.order_id

    def get_status(self) -> str:
        return self.status

    def is_assigned(self):
        return self.courier is not None

    def __str__(self):
        return (
            f"Order ID: {self.order_id}\n"
            f"Customer ID: {self.customer_id}\n"
            f"Destination: {self.destination}\n"
            f"Status: {self.status}"
        )

    def __repr__(self):
        return f"Order(order_id={self.order_id}, customer_id={self.customer_id}, destination='{self.destination}', status='{self.status}')"

    def update_status(self, new_status: str):
        self.status = new_status

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "pickup_address": self.pickup_address,
            "item_description": self.item_description,
            "destination": self.destination,
            "status": self.status,
            "courier_id": self.courier_id,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S")
        }

    @classmethod
    def from_dict(cls, data):
        order = cls(
            order_id=data["order_id"],
            customer_id=data["customer_id"],
            destination=data["destination"],
            customer_name=data.get("customer_name"),
            pickup_address=data.get("pickup_address"),
            item_description=data.get("item_description")
        )
        order.status = data.get("status", "pending")
        order.courier_id = data.get("courier_id")
        order.date = datetime.strptime(data.get("date", datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S")
        return order
