
from collections import defaultdict
import Courier as courier
import Order as order
import heapq
orders = []

<<<<<<< Updated upstream

def __init__(self):
        self.orders = []
        self.couriers = []
        self.load_couriers_from_file()
        self.load_orders_from_file()



=======
class DispatchSystem:
    def __init__(self):
        self.orders = []
        self.couriers = []
>>>>>>> Stashed changes




def assign_order_to_courier(order_id, courier_id):
    for o in orders:
        if o.order_id == order_id:
            courier_obj = courier.find_courier_by_id(courier_id)
            if courier_obj and not o.is_assigned():
                o.assign_to(courier_obj)
                print(f"Order {order_id} assigned to courier {courier_obj.name}.")
            

def get_average_delivery_time():
    total_time = 0
    delivered_orders = 0

    for o in orders:
        if o.is_delivered():
            total_time += o.delivery_time
            delivered_orders += 1

    if delivered_orders == 0:
        return 0

    return total_time / delivered_orders


def load_couriers_from_file(self, filename="couriers.json"):
        import json, os
        if not os.path.exists(filename):
            return
        
        with open(filename, "r") as f:

            data = json.load(f)

            for entry in data:
                c = courier.Courier(entry["name"], entry["courier_id"], entry["region"])
                c.deliveries = entry.get("deliveries", [])
                self.couriers.append(c)
        




def build_courier_load_heap(orders):
    courier_order_counts = defaultdict(int)

    for order in orders:
        if order.courier:
            courier_id = order.courier.courier_id
            courier_order_counts[courier_id] += 1

   
    courier_heap = [(num_orders, courier_id) for courier_id, num_orders in courier_order_counts.items()]
    heapq.heapify(courier_heap)

    return courier_heap

# --------- order management functions ---------


def load_orders_from_file(self, filename="orders.json"):
        import json, os
        if not os.path.exists(filename):
            return
        with open(filename, "r") as f:
            data = json.load(f)
            for entry in data:
                o = order.Order(entry["customer_id"], entry["destination"])
                o.order_id = entry["order_id"]
                o.status = entry["status"]
                o.date = entry["date"]
                courier_id = entry.get("courier_id")
                if courier_id:
                    o.courier = self.find_courier_by_id(courier_id)
                self.orders.append(o)



def add_order(self, order_id, customer_name, delivery_address):
    new_order = order.Order(order_id, customer_name, delivery_address)
    self.orders.append(new_order)
    print(f"Order {order_id} added for {customer_name} at {delivery_address}.")



def add_order_by_customer(order_id, customer_name, delivery_address):
    if not any(o.order_id == order_id for o in orders):
        add_order(order_id, customer_name, delivery_address)
    else:
        print(f"Order {order_id} already exists. Please use a different order ID.")

def auto_assign_orders():
    for o in orders:
        if not o.is_assigned():
            available_courier = courier.find_available_courier()
            if available_courier:
                o.assign_to(available_courier)
                print(f"Order {o.order_id} assigned to courier {available_courier.name}.")
            else:
                print(f"No available couriers for order {o.order_id}.")

def get_active_orders(self):
    return [o for o in self.orders if o.status != 'delivered' and o.status != 'cancelled']

def update_order_status(self, order_id, new_status):
        for o in self.orders:
            if o.order_id == order_id:
                o.update_status(new_status)
                print(f"Order {order_id} status updated to {new_status}")
                return
        print(f"Order {order_id} not found.")

def get_orders_for_courier(self, courier_id):
    return [o for o in self.orders if o.courier and o.courier.courier_id == courier_id]


#------------ COURIERS ------------


def add_courier(self, courier):
        self.couriers.append(courier)
        print(f"Courier {courier.name} (ID: {courier.courier_id}) added.")
        self.save_couriers_to_file()
        
def find_courier_by_id(self, courier_id):
        for c in self.couriers:
            if c.courier_id == courier_id:
                return c
        return None
    
    

def find_available_courier(self):
        if not self.couriers:
            return None
        return min(self.couriers, key=lambda c: len(c.deliveries))

def get_active_couriers(self):
        return [c for c in self.couriers if len(c.deliveries) > 0]

def get_all_couriers(self):
        return self.couriers

def get_region_loads(self):
        region_counts = defaultdict(int)
        for o in self.orders:
            if o.courier:
                region_counts[o.courier.courier_region] += 1
        return dict(region_counts)

def get_average_delivery_time(self):
        total_time = 0
        delivered_orders = 0
        for o in self.orders:
            if hasattr(o, 'delivery_time'):
                total_time += o.delivery_time
                delivered_orders += 1
        return total_time / delivered_orders if delivered_orders > 0 else 0

   