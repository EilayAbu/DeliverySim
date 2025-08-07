from Courier import Courier
from Customer import Customer
from Order import Order
from Manager import Manager
from DispatchSystem import DispatchSystem  # updated import
# Global instance of dispatch system
dispatch_system = DispatchSystem()

# Load existing orders from file if available
dispatch_system.load_orders_from_file()

# Placeholder for couriers and customers
couriers = {}
customers = {}


def customer_menu():
    user
    print("\n--- Customer Menu ---")
    choice = int(input("Enter your customer ID (or 0 to create new): "))
    if choice == 0:
        name = input("Enter your name: ")
        password = input("Enter your password: ")
        address = input("Enter your address: ")
        phone = input("Enter your phone number: ")
        customer_id = int(input("Enter a unique customer ID: "))

        while customer_id in customers:
            print("Customer ID already exists. Please try again.")
            customer_id = int(input("Enter a unique customer ID: "))

        user = Customer(customer_id, name, password, address, phone)
        customers.append(user)
        print(f"Customer created with ID: {customer_id}")
    elif customer_id not in customers:
        print("Customer not found.")
        return

    while True:
        print("1. Create new order")
        print("2. Check order status")
        print("3. Back")
        choice = input("Choose an option: ")

        if choice == "1":
            destination = input("Enter delivery destination: ")
            order = Order(Order.generate_unique_order_id(), customer_id, destination)
            dispatch_system.add_order(order)
            dispatch_system.save_orders_to_file()  # save to JSON
            print(f"Order created. Order ID: {order.get_order_id()}")
        elif choice == "2":
            order_id = int(input("Enter your order ID: "))
            for o in dispatch_system.orders:
                if o.get_order_id() == order_id:
                    print(o)
                    break
            else:
                print("Order not found.")
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


def courier_menu():
    print("\n--- Courier Menu ---")
    courier_id = int(input("Enter your courier ID: "))
    courier_obj = dispatch_system.find_courier_by_id(courier_id)
    if not courier_obj:
        print("Courier not found.")
        return

    while True:
        print("1. View assigned orders")
        print("2. Update order status")
        print("3. Back")
        choice = input("Choose an option: ")

        if choice == "1":
            for order in dispatch_system.orders:
                if getattr(order, 'courier', None) == courier_obj:
                    print(order)
        elif choice == "2":
            order_id = int(input("Enter order ID: "))
            new_status = input("Enter new status (picked_up/in_transit/delivered): ")
            for o in dispatch_system.orders:
                if o.get_order_id() == order_id:
                    o.update_status(new_status)
                    dispatch_system.save_orders_to_file()  # save update
                    print("Status updated.")
                    break
            else:
                print("Order not found.")
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


def manager_menu():
    print("\n--- Manager Menu ---")
    manager = Manager("System Manager", dispatch_system)
    while True:
        print("1. View active orders")
        print("2. Manually assign order")
        print("3. Auto assign orders")
        print("4. View analytics")
        print("5. Back")
        choice = input("Choose an option: ")

        if choice == "1":
            active_orders = manager.view_active_orders()
            for o in active_orders:
                print(o)
        elif choice == "2":
            order_id = int(input("Enter order ID: "))
            courier_id = int(input("Enter courier ID: "))
            manager.manually_assign_order(order_id, courier_id)
            dispatch_system.save_orders_to_file()
        elif choice == "3":
            manager.auto_assign_orders()
            dispatch_system.save_orders_to_file()
        elif choice == "4":
            analytics = manager.get_analytics()
            for key, value in analytics.items():
                print(f"{key}: {value}")
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


def main():
    while True:
        print("\n=== Welcome to DeliverySim ===")
        print("1. Customer")
        print("2. Courier")
        print("3. Manager")
        print("4. Exit")
        choice = input("Select your role: ")

        if choice == "1":
            customer_menu()
        elif choice == "2":
            courier_menu()
        elif choice == "3":
            manager_menu()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
