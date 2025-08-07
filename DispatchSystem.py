from customer_utils import (
    add_customer,
    update_customer,
    delete_customer,
    get_customer_by_id,
    get_all_customers,
    customer_exists
)
from courier_utils import (
    add_courier,
    update_courier,
    delete_courier,
    get_courier_by_id,
    get_all_couriers,
    courier_exists
)
from collections import defaultdict
import Courier as courier
import Order as order
import json
import os

class DispatchSystem:
    def __init__(self):
        self.orders = []
        self.couriers = []
        self.load_couriers_from_file()
        self.load_orders_from_file()

    def get_average_delivery_time(self):
        total_delivery_time = 0
        delivered_order_count = 0
        for order_object in self.orders:
            if order_object.is_delivered():
                total_delivery_time += order_object.delivery_time
                delivered_order_count += 1
        if delivered_order_count == 0:
            return 0
        return total_delivery_time / delivered_order_count

    def load_couriers_from_file(self, filename="couriers.json"):
        if not os.path.exists(filename):
            return
        with open(filename, "r") as file:
            data = json.load(file)
            for entry in data:
                courier_instance = courier.Courier(entry["name"], entry["courier_id"], entry["region"])
                courier_instance.deliveries = entry.get("deliveries", [])
                self.couriers.append(courier_instance)

    def load_orders_from_file(self, filename="orders.json"):
        if not os.path.exists(filename):
            return
        with open(filename, "r") as file:
            data = json.load(file)
            for entry in data:
                order_instance = order.Order(entry["order_id"], entry["customer_id"], entry.get("pickup_location", ""), entry["destination"])
                order_instance.status = entry["status"]
                order_instance.date = entry["date"]
                courier_id = entry.get("courier_id")
                if courier_id:
                    order_instance.courier = self.find_courier_by_id(courier_id)
                self.orders.append(order_instance)

    def save_orders_to_file(self, filename="orders.json"):
        order_data_list = []
        for order_instance in self.orders:
            order_data_list.append({
                "order_id": order_instance.order_id,
                "customer_id": order_instance.customer_id,
                "pickup_location": getattr(order_instance, "pickup_location", ""),
                "destination": order_instance.destination,
                "status": order_instance.status,
                "date": str(order_instance.date),
                "courier_id": order_instance.courier.courier_id if order_instance.courier else None
            })
        with open(filename, "w") as file:
            json.dump(order_data_list, file, indent=4)

    def add_order(self, order_instance):
        for existing_order in self.orders:
            if existing_order.order_id == order_instance.order_id:
                print(f"Order {order_instance.order_id} already exists.")
                return
        self.orders.append(order_instance)
        self.save_orders_to_file()
        print(f"Order {order_instance.order_id} added.")

    def add_courier(self, courier_instance):
        if any(existing_courier.courier_id == courier_instance.courier_id for existing_courier in self.couriers):
            print(f"Courier {courier_instance.courier_id} already exists.")
            return
        add_courier(courier_instance)
        self.couriers.append(courier_instance)
        print(f"Courier {courier_instance.name} added and saved.")

    def find_courier_by_id(self, courier_id):
        for courier_instance in self.couriers:
            if courier_instance.courier_id == courier_id:
                return courier_instance
        return None

    def assign_order_to_courier(self, order_id, courier_id):
        courier_instance = self.find_courier_by_id(courier_id)
        for order_instance in self.orders:
            if order_instance.order_id == order_id and courier_instance:
                order_instance.courier = courier_instance
                courier_instance.assign_order(order_id)
                print(f"Order {order_id} assigned to courier {courier_instance.name}.")
                self.save_orders_to_file()
                return
        print(f"Order or courier not found.")

    def auto_assign_orders(self):
        for order_instance in self.orders:
            if not order_instance.is_assigned():
                available_couriers = self.get_available_couriers()
                if available_couriers:
                    courier_instance = available_couriers[0]
                    order_instance.assign_to(courier_instance)
                    print(f"Order {order_instance.order_id} assigned to courier {courier_instance.name}.")
        self.save_orders_to_file()

    def courier_update_status(self, courier_id, order_id, new_status):
        courier_instance = self.find_courier_by_id(courier_id)
        if not courier_instance:
            print(f"Courier {courier_id} not found.")
            return
        for order_instance in self.orders:
            if order_instance.order_id == order_id:
                if order_instance.courier is None:
                    print(f"Order {order_id} is not assigned to any courier.")
                    return
                elif order_instance.courier.courier_id != courier_id:
                    print(f"Order {order_id} is not assigned to courier {courier_instance.name}.")
                    return
                order_instance.update_status(new_status)
                print(f"Order {order_id} status updated to '{new_status}' by courier {courier_instance.name}.")
                self.save_orders_to_file()
                return
        print(f"Order {order_id} not found.")

    def update_order_status(self, order_id, new_status):
        for order_instance in self.orders:
            if order_instance.order_id == order_id:
                order_instance.update_status(new_status)
                print(f"Order {order_id} status updated to {new_status}")
                self.save_orders_to_file()
                return
        print(f"Order {order_id} not found.")

    def get_orders_for_courier(self, courier_id):
        return [order_instance for order_instance in self.orders if order_instance.courier and order_instance.courier.courier_id == courier_id]

    def get_active_orders(self):
        return [order_instance for order_instance in self.orders if order_instance.status not in ('delivered', 'cancelled')]

    def get_available_couriers(self, max_deliveries=3):
        return [courier_instance for courier_instance in self.couriers if len(courier_instance.deliveries) < max_deliveries]

    def get_active_couriers(self):
        return [courier_instance for courier_instance in self.couriers if len(courier_instance.deliveries) > 0]

    def get_all_couriers(self):
        return self.couriers

    def get_region_loads(self):
        region_counts = defaultdict(int)
        for order_instance in self.orders:
            if order_instance.courier:
                region_counts[order_instance.courier.courier_region] += 1
        return dict(region_counts)

    def history_of_orders_by_customer(self, customer_id):
        return [order_instance for order_instance in self.orders if order_instance.customer_id == customer_id]
