from datetime import datetime
# create a class Order with the following attributes:
# - order_id: int where the order ID is unique
# - customer_id: int
# - destination: str
# - status: str (e.g., 'pending', 'delivered', 'cancelled')
class Order:
    _next_order_id = 1

    def __init__(self, customer_id: int, destination: str):
        self.order_id = Order._next_order_id
        Order._next_order_id += 1
        self.customer_id = customer_id
        self.destination = destination
        self.status = 'pending'  # Default status
        self.date = datetime.now()


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
