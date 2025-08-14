# ---------------------- IMPORTS ----------------------

from Customer import Customer
from Courier import Courier
from Order import Order, generate_unique_order_id
from Manager import Manager
from DispatchSystem import DispatchSystem
from customer_utils import get_customer_by_id, add_customer
from courier_utils import get_courier_by_id

# ---------------------- GLOBAL STATE ----------------------

dispatch_system = DispatchSystem()
user = None


# ---------------------- ENTRY POINT ----------------------

def main():
    global user
    while True:
        print("\n=== Welcome to DeliverySim ===")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            user = login()
        elif choice == "2":
            user = register()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

        if user:
            route_by_role(user)


# ---------------------- AUTH & ROUTING ----------------------

def login():
    print("\n--- Login ---")
    user_id = int(input("Enter your ID: "))

    while True:
        role = input("Enter your role (customer / courier / manager): ").lower()
        if role in ["customer", "courier", "manager"]:
            break
        print("Invalid role. Please try again.")

    if role == "customer":
        data = get_customer_by_id(user_id)
        if not data:
            print("Customer not found.")
            return None
        print(f"Welcome back, {data['name']}")
        return Customer(**data)

    elif role == "courier":
        data = get_courier_by_id(user_id)
        if not data:
            print("Courier not found.")
            return None
        print(f"Welcome back, {data['name']}")
        return Courier(data['name'], data['courier_id'], data['region'])

    elif role == "manager":
        print("Manager access granted.")
        return Manager("System Manager", dispatch_system)


def register():
    print("\n--- Register ---")
    role = input("Registering as (customer / courier): ").lower()
    name = input("Enter your name: ")
    id_value = int(input("Choose a unique ID: "))

    if role == "customer":
        password = input("Enter your password: ")
        address = input("Enter your address: ")
        phone = input("Enter your phone number: ")
        if get_customer_by_id(id_value):
            print("Customer ID already exists.")
            return None
        customer = Customer(id_value, name, password, address, phone)
        add_customer(customer)
        print(f"Customer {id_value} added.")
        return customer

    elif role == "courier":
        region = input("Enter your delivery region: ")
        if get_courier_by_id(id_value):
            print("Courier ID already exists.")
            return None
        courier = Courier(name, id_value, region)
        dispatch_system.add_courier(courier)
        print(f"Courier {id_value} added.")
        return courier

    else:
        print("Invalid role.")
        return None


def route_by_role(user):
    if isinstance(user, Customer):
        menu_for_customer(user)
    elif isinstance(user, Courier):
        menu_for_courier(user)
    elif isinstance(user, Manager):
        menu_for_manager()


# ---------------------- CUSTOMER FLOW ----------------------

def menu_for_customer(customer):
    while True:
        print("\n--- Customer Menu ---")
        print("1. Create new order")
        print("2. View my active orders")
        print("3. View my order history")
        print("4. Back")
        choice = input("Choose an option: ")

        if choice == "1":
            create_customer_order(customer)

        elif choice == "2":
            active_orders = dispatch_system.get_active_orders()
            filtered_orders = [
                order for order in active_orders if order.customer_id == customer.customer_id
            ]
            if not filtered_orders:
                print("You have no active orders.")
            else:
                for order in filtered_orders:
                    print(f"order_id={order.order_id}, pickup={order.pickup_location}, destination={order.destination}, status={order.status}, date={order.date}, courier_id={getattr(order.courier, 'courier_id', None)}")

        elif choice == "3":
            order_history = dispatch_system.history_of_orders_by_customer(customer.customer_id)
            if not order_history:
                print("You have no past orders.")
            else:
                for order in order_history:
                    print(order)

        elif choice == "4":
            break
        else:
            print("Invalid choice.")


def create_customer_order(customer):
    print("\n--- New Order ---")
    print("Where should we pick up the package?")
    print("1. From MY address")
    print("2. From a DIFFERENT address")
    pickup_choice = input("Choose an option: ")

    if pickup_choice == "1":
        pickup_location = customer.address
    elif pickup_choice == "2":
        pickup_location = input("Enter pickup address: ")
    else:
        print("Invalid choice.")
        return

    destination = input("Enter destination address: ")
    order_id = generate_unique_order_id()

    order = Order(order_id, customer.customer_id, pickup_location, destination)
    dispatch_system.add_order(order)
    print(f"Order {order_id} created successfully.")


# ---------------------- COURIER FLOW ----------------------

def menu_for_courier(courier):
    while True:
        print("\n--- Courier Menu ---")
        print("1. View new orders assigned to you")
        print("2. Update order status")
        print("3. Back")
        choice = input("Choose an option: ")

        if choice == "1":
            assigned_orders = dispatch_system.get_orders_for_courier(courier.courier_id)
            if not assigned_orders:
                print("No orders assigned to you.")
            for order in assigned_orders:
                print(f"order_id={order.order_id}, pickup={order.pickup_location}, destination={order.destination}, status={order.status}, date={order.date}, customer_id={order.customer_id}")

        elif choice == "2":
            order_id = int(input("Enter order ID: "))
            new_status = input("Enter new status (picked_up / in_transit / delivered): ")
            dispatch_system.courier_update_status(courier.courier_id, order_id, new_status)

        elif choice == "3":
            break
        else:
            print("Invalid choice.")


# ---------------------- MANAGER FLOW ----------------------

def menu_for_manager():
    while True:
        print("\n--- Manager Menu ---")
        print("1. Register new courier")
        print("2. View all active orders")
        print("3. Manually assign courier")
        print("3a. Assign NEAREST courier automatically")
        print("4. View delivery time analytics")
        print("5. Back")
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Courier name: ")
            courier_id = int(input("Courier ID: "))
            region = input("Courier region: ")
            location = input("Courier base/current address (for nearest-pickup): ")
            courier = Courier(name, courier_id, region, location)
            dispatch_system.add_courier(courier)    

        elif choice == "2":
            active_orders = dispatch_system.get_active_orders()
            for order in active_orders:
                print(f"order_id={order.order_id}, pickup={order.pickup_location}, destination={order.destination}, status={order.status}, date={order.date}, courier_id={getattr(order.courier, 'courier_id', None)}, customer_id={order.customer_id}")

        elif choice == "3":
            order_id = int(input("Enter order ID to assign: "))
            courier_id = int(input("Enter courier ID to assign: "))
            dispatch_system.assign_order_to_courier(order_id, courier_id)
        
        elif choice.lower() == "3a":
            order_id = int(input("Enter order ID to auto-assign nearest: "))
            dispatch_system.assign_nearest_courier(order_id)

        elif choice == "4":
            avg_time = dispatch_system.get_average_delivery_time()
            print(f"Average delivery time: {avg_time:.2f} units")

        elif choice == "5":
            break
        else:
            print("Invalid choice.")


# ---------------------- RUN ----------------------

if __name__ == "__main__":
    main()
