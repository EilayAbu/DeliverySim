
from collections import defaultdict
import Courier as courier
import Order as order
import heapq
orders = []



def add_order(order_id, customer_name, delivery_address):
    new_order = order.Order(order_id, customer_name, delivery_address)
    orders.append(new_order)
    print(f"Order {order_id} added for {customer_name} at {delivery_address}.")

def auto_assign_orders():
    for o in orders:
        if not o.is_assigned():
            available_courier = courier.find_available_courier()
            if available_courier:
                o.assign_to(available_courier)
                print(f"Order {o.order_id} assigned to courier {available_courier.name}.")
            else:
                print(f"No available couriers for order {o.order_id}.")

def add_order_by_customer(order_id, customer_name, delivery_address):
    if not any(o.order_id == order_id for o in orders):
        add_order(order_id, customer_name, delivery_address)
    else:
        print(f"Order {order_id} already exists. Please use a different order ID.")

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



def build_courier_load_heap(orders):
    courier_order_counts = defaultdict(int)

    for order in orders:
        if order.courier:
            courier_id = order.courier.courier_id
            courier_order_counts[courier_id] += 1

   
    courier_heap = [(num_orders, courier_id) for courier_id, num_orders in courier_order_counts.items()]
    heapq.heapify(courier_heap)

    return courier_heap

