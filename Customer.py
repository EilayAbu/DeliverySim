import uuid

class Customer:
    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone
        self.orders = {}

    def create_order(self, destination):
        delivery_id = str(uuid.uuid4())
        self.orders[delivery_id] = {
            "sender": {
                "name": self.name,
                "address": self.address,
                "phone": self.phone
            },
            "destination": destination,
            "status": "Created"
        }
        return delivery_id

    def check_status(self, delivery_id):
        order = self.orders.get(delivery_id)
        if order:
            return order["status"]
        else:
            return "Invalid delivery ID"