# create a class Order with the following attributes:
# - order_id: int where the order ID is unique
# - customer_id: int
# - destination: str
# - status: str (e.g., 'pending', 'delivered', 'cancelled')
class Order:
    _next_order_id = 1

    def __init__(self, customer_id: int, destination: str, status: str):
        self.order_id = Order._next_order_id
        Order._next_order_id += 1
        self.customer_id = customer_id
        self.destination = destination
        self.status = status

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
