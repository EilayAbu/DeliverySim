from Customer import Customer
from Courier import Courier
from Manager import Manager
from Order import Order
from DispatchSystem import DispatchSystem
import os
import json


import json

def customer_menu(dispatch_system):
    print("\n--- Customer Menu ---")
    name = input("Enter your name: ")
    address = input("Enter your address: ")
    phone = input("Enter your phone: ")
    customer = Customer(name=name, address=address, phone=phone)

    destination = input("Enter delivery destination: ")
    item = input("Enter item description: ")
    new_order = customer.create_order(destination, item)
    save_order_to_file(new_order)

    
    dispatch_system.add_order(new_order)
    print(f"Order created! ID: {new_order.order_id}")
    
    check = input("Do you want to check the status of an order? (y/n): ").lower()
    if check == "y":
        order_id = int(input("Enter your order ID: "))
        status = get_order_status_from_file(order_id)
        if status:
            print(f"Status of order {order_id}: {status}")
        else:
            print("Order not found.")

def get_order_status_from_file(order_id, filename="orders.json"):
    if not os.path.exists(filename):
        return None
    with open(filename, "r") as f:
        try:
            orders = json.load(f)
            for order in orders:
                if order["order_id"] == order_id:
                    return order["status"]
        except json.JSONDecodeError:
            return None
    return None

def save_order_to_file(order, filename="orders.json"):
    data = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

    data.append({
        "order_id": order.order_id,
        "customer_id": order.customer_id,
        "destination": order.destination,
        "status": order.status,
        "date": str(order.date)
    })

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def courier_menu(dispatch_system):
    print("\n--- Courier Menu ---")
    courier_id = int(input("Enter your courier ID: "))
    courier = dispatch_system.find_courier_by_id(courier_id)

    if not courier:
        print("❌ Courier not found.")
        return

    print(f"Welcome {courier.name}!")
    orders = dispatch_system.get_orders_for_courier(courier_id)
    if not orders:
        print("You have no assigned deliveries.")
        return

    for o in orders:
        print(f"\nOrder ID: {o.order_id}, Status: {o.status}, Destination: {o.destination}")

    choice = input("\nDo you want to update an order status? (y/n): ").lower()
    if choice == "y":
        order_id = int(input("Enter order ID: "))
        new_status = input("Enter new status (picked_up/in_transit/delivered): ")
        dispatch_system.update_order_status(order_id, new_status)



def manager_menu(dispatch_system):
    print("\n--- Manager Menu ---")
    manager = Manager(name="System Manager", dispatch_system=dispatch_system)
    
    print("1. View active orders")
    print("2. Auto-assign orders")
    print("3. View analytics")
    print("4. View all couriers")
    print("5. Add new courier")
    choice = input("Choose: ")

    if choice == "1":
        for order in manager.view_active_orders():
            print(order)
    elif choice == "2":
        manager.auto_assign_orders()
    elif choice == "3":
        analytics = manager.get_analytics()
        print(analytics)
    elif choice == "4":
        print("\nAll couriers:")
        for c in dispatch_system.get_all_couriers():
            in_shift = "✅ In shift" if len(c.deliveries) > 0 else "❌ Not in shift"
            print(f"Courier ID: {c.courier_id}, Name: {c.name}, Region: {c.courier_region}, {in_shift}")
    elif choice == "5":
        print("\n--- Add New Courier ---")
        name = input("Courier name: ")
        courier_id = int(input("Courier ID (must be unique): "))
        region = input("Courier region: ")
        from Courier import Courier
        new_courier = Courier(name=name, courier_id=courier_id, courier_region=region)
        dispatch_system.add_courier(new_courier)
        print(f"Courier {name} added successfully.")


def main():
    from DispatchSystem import DispatchSystem
    dispatch_system = DispatchSystem()

    while True:
        print("\nWelcome to DeliverySim")
        print("1. Customer")
        print("2. Courier")
        print("3. Manager")
        print("0. Exit")
        choice = input("Choose role: ")

        if choice == "1":
            customer_menu(dispatch_system)
        elif choice == "2":
            courier_menu(dispatch_system)
        elif choice == "3":
            manager_menu(dispatch_system)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

