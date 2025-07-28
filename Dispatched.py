from collections import defaultdict
import heapq
import json
from Order import Order

class Dispatched:
    def __init__(self):
        self.orders = []
        self.couriers = []

    def add_order(self, order):
        self.orders.append(order)
        print(f"Order {order.order_id} added for customer {order.customer_id} to {order.destination}.")

    def auto_assign_orders(self):
        for o in self.orders:
            if not hasattr(o, 'courier') or o.courier is None:
                available_courier = self.find_available_courier()
                if available_courier:
                    o.courier = available_courier
                    available_courier.assign_order(o.order_id)
                    print(f"Order {o.order_id} assigned to courier {available_courier.name}.")
                else:
                    print(f"No available couriers for order {o.order_id}.")

    def assign_order_to_courier(self, order_id, courier_id):
        for o in self.orders:
            if o.order_id == order_id:
                courier_obj = self.find_courier_by_id(courier_id)
                if courier_obj and not hasattr(o, 'courier'):
                    o.courier = courier_obj
                    courier_obj.assign_order(order_id)
                    print(f"Order {order_id} assigned to courier {courier_obj.name}.")

    def get_average_delivery_time(self):
        total_time = 0
        delivered_orders = 0
        for o in self.orders:
            if hasattr(o, 'delivery_time') and o.status == 'delivered':
                total_time += o.delivery_time
                delivered_orders += 1
        return total_time / delivered_orders if delivered_orders else 0

    def build_courier_load_heap(self):
        courier_order_counts = defaultdict(int)
        for order in self.orders:
            if hasattr(order, 'courier'):
                courier_id = order.courier.courier_id
                courier_order_counts[courier_id] += 1
        courier_heap = [(num_orders, courier_id) for courier_id, num_orders in courier_order_counts.items()]
        heapq.heapify(courier_heap)
        return courier_heap

    def find_courier_by_id(self, courier_id):
        for c in self.couriers:
            if c.courier_id == courier_id:
                return c
        return None

    def get_active_orders(self):
        return [o for o in self.orders if o.status != 'delivered']

    def get_region_loads(self):
        region_count = defaultdict(int)
        for o in self.orders:
            if hasattr(o, 'courier'):
                region = o.courier.courier_region
                region_count[region] += 1
        return dict(region_count)

    def get_active_couriers(self):
        return [c for c in self.couriers if c.deliveries]

    def add_courier(self, courier):
        self.couriers.append(courier)

    def save_orders_to_file(self, filename="orders.json"):
        with open(filename, "w") as f:
            json.dump([o.to_dict() for o in self.orders], f, indent=4)

    def load_orders_from_file(self, filename="orders.json"):
        try:
            with open(filename, "r") as f:
                orders_data = json.load(f)
                for o in orders_data:
                    order = Order(o['customer_id'], o['destination'])
                    order.order_id = o['order_id']
                    order.status = o['status']
                    self.orders.append(order)
        except FileNotFoundError:
            print("No existing orders file found.")
