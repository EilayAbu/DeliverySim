class Courier:
    def __init__(self, name: str, courier_id: int, courier_region: str):
        self.name = name
        self.courier_id = courier_id
        self.courier_region = courier_region
        self.deliveries = []

    def assign_order(self, order_id: int):
        self.deliveries.append(order_id)

    def complete_order(self, order_id: int):
        if order_id in self.deliveries:
            self.deliveries.update(order_id, status='delivered')

    def __repr__(self):
        return f"Courier(name={self.name}, courier_id={self.courier_id}, deliveries={len(self.deliveries)})"
    


