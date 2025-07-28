from datetime import datetime
# create a class Order with the following attributes:
# - order_id: int where the order ID is unique
# - customer_id: int
# - destination: str
# - status: str (e.g., 'pending', 'delivered', 'cancelled')

import random
import json
import os

# === טוען את כל המזהים הקיימים מקובץ JSON ===
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

# מזהים קיימים נטענים פעם אחת
existing_order_ids = load_existing_order_ids()

# === יוצר מזהה ייחודי בן 6 ספרות ===
def generate_unique_order_id():
    while True:
        order_id = random.randint(100000, 999999)
        if order_id not in existing_order_ids:
            existing_order_ids.add(order_id)
            return order_id
class Order:
    _next_order_id = 1

    # def __init__(self, customer_id: int, destination: str):
    #     self.order_id = Order._next_order_id
    #     Order._next_order_id += 1
    #     self.customer_id = customer_id
    #     self.destination = destination
    #     self.status = 'pending'  # Default status
    #     self.date = datetime.now()
    #     self.courier = None  # ← שורה חשובה שחסרה -added by avital

    def __init__(self, customer_id, destination):
        self.order_id = generate_unique_order_id()
        self.customer_id = customer_id
        self.destination = destination
        self.status = 'pending'
        self.date = datetime.now()
        self.courier = None

        # save in a json file
        import json
        import os
        orders_file = 'orders.json'

    def get_order_id(self) -> int:
        return self.order_id

    def get_status(self) -> str:
        return self.status

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
    
    #sprint 2
    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "destination": self.destination,
            "status": self.status,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S")
        }
