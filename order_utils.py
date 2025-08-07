import json
import os
from Order import Order
from courier_utils import get_courier_by_id

FILENAME = "data/orders.json"

def _load_all_orders():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("Warning: Corrupted orders file. Returning empty list.")
            return []

def _save_all_orders(orders):
    os.makedirs(os.path.dirname(FILENAME), exist_ok=True)
    with open(FILENAME, "w") as f:
        json.dump(orders, f, indent=4)

def get_all_orders():
    return _load_all_orders()

def get_order_by_id(order_id):
    orders = _load_all_orders()
    for o in orders:
        if o["order_id"] == order_id:
            return o
    return None

def order_exists(order_id):
    return get_order_by_id(order_id) is not None

def add_order(order):
    orders = _load_all_orders()
    if order_exists(order.order_id):
        print(f"Order {order.order_id} already exists.")
        return
    orders.append({
        "order_id": order.order_id,
        "customer_id": order.customer_id,
        "pickup_location": order.pickup_location,
        "destination": order.destination,
        "status": order.status,
        "date": str(order.date),
        "courier_id": order.courier.courier_id if order.courier else None
    })
    _save_all_orders(orders)
    print(f"Order {order.order_id} added.")

def update_order(order):
    orders = _load_all_orders()
    for i, o in enumerate(orders):
        if o["order_id"] == order.order_id:
            orders[i] = {
                "order_id": order.order_id,
                "customer_id": order.customer_id,
                "destination": order.destination,
                "status": order.status,
                "date": str(order.date),
                "courier_id": order.courier.courier_id if order.courier else None
            }
            _save_all_orders(orders)
            print(f"Order {order.order_id} updated.")
            return
    print("Order not found for update.")

def delete_order(order_id):
    orders = _load_all_orders()
    new_orders = [o for o in orders if o["order_id"] != order_id]
    if len(new_orders) == len(orders):
        print("Order not found.")
        return
    _save_all_orders(new_orders)
    print(f"Order {order_id} deleted.")
