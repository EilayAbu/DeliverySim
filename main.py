import json
import os
import uuid
from DispatchSystem import DispatchSystem
from Customer import Customer
from Courier import Courier
from Manager import Manager

USERS_FILE = "users.json"
dispatch_system = DispatchSystem()

# --- Persistence ---
def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# --- Initial Setup ---
def ensure_manager():
    users = load_users()
    if not any(u for u in users if u["role"] == "manager"):
        users.append({
            "user_id": "admin001",
            "name": "Admin",
            "phone": "admin",
            "password": "admin123",
            "role": "manager"
        })
        save_users(users)

# --- User Management ---
def sign_up():
    print("\n--- Sign Up (Customers only) ---")
    name = input("Full name: ")
    address = input("Address: ")
    phone = input("Phone: ")
    password = input("Password: ")

    users = load_users()
    if any(u["phone"] == phone for u in users):
        print("\n⚠️ User already exists.")
        return None

    user = {
        "user_id": str(uuid.uuid4())[:8],
        "name": name,
        "phone": phone,
        "password": password,
        "address": address,
        "role": "customer"
    }
    users.append(user)
    save_users(users)
    print("\n✅ Registered successfully.")
    return user

def sign_in():
    print("\n--- Sign In ---")
    phone = input("Phone: ")
    password = input("Password: ")
    users = load_users()
    for user in users:
        if user["phone"] == phone and user["password"] == password:
            print(f"\n👋 Welcome {user['name']}!")
            return user
    print("\n❌ Invalid credentials.")
    return None

# --- Role Menus ---
def customer_menu(user):
    customer = Customer(user["name"], user["address"], user["phone"], user["password"])
    while True:
        print("\n--- Customer Menu ---")
        print("1. Create new order")
        print("2. View order history")
        print("3. View active orders")
        print("0. Logout")
        choice = input("Choose: ")
        if choice == "1":
            destination = input("Enter delivery destination: ")
            item = input("Enter item description: ")
            order = customer.create_order(destination, item)
            dispatch_system.add_order(order)
            print(f"\n📦 Order created! ID: {order.order_id}")
        elif choice == "2":
            for order in dispatch_system.history_of_orders_by_customer(customer.customer_id):
                print(order)
        elif choice == "3":
            for order in dispatch_system.get_active_orders():
                print(order)
        elif choice == "0":
            print("\n👋 Logged out from customer account.")
            break
        else:
            print("\n❌ Invalid option.")



def courier_menu(user):
    courier_id = int(user["user_id"][-3:], 16) % 1000
    courier = dispatch_system.find_courier_by_id(courier_id)
    if not courier:
        courier = Courier(user["name"], courier_id, "default")
        dispatch_system.add_courier(courier)
    while True:
        print("\n--- Courier Menu ---")
        print("1. View assigned deliveries")
        print("0. Logout")
        choice = input("Choose: ")
        if choice == "1":
            orders = dispatch_system.get_orders_for_courier(courier_id)
            if not orders:
                print("\nNo deliveries assigned.")
            else:
                for o in orders:
                    print(f"\nOrder ID: {o.order_id}, Status: {o.status}, Destination: {o.destination}")
                if input("Update order status? (y/n): ").lower() == 'y':
                    oid = int(input("Order ID: "))
                    status = input("New status (picked_up/in_transit/delivered): ")
                    dispatch_system.update_order_status(oid, status)
        elif choice == "0":
            print("\n👋 Logged out from courier account.")
            break
        else:
            print("\n❌ Invalid option.")



def manager_menu():
    print("\n--- Manager Menu ---")
    manager = Manager("System Manager", dispatch_system)
    while True:
        print("\n1. View active orders")
        print("2. Auto-assign orders")
        print("3. Add new courier")
        print("4. View all couriers")
        print("0. Logout")
        choice = input("Choose: ")
        if choice == "1":
            for order in manager.view_active_orders():
                print(order)
        elif choice == "2":
            manager.auto_assign_orders()
        elif choice == "3":
            name = input("Courier name: ")
            phone = input("Courier login: ")
            password = input("Courier password: ")
            users = load_users()
            user = {
                "user_id": str(uuid.uuid4())[:8],
                "name": name,
                "phone": phone,
                "password": password,
                "role": "courier"
            }
            users.append(user)
            save_users(users)
            print(f"Courier {name} added.")
        elif choice == "4":
            users = load_users()
            print("\n--- Couriers List ---")
            for u in users:
                if u["role"] == "courier":
                    print(f"Name: {u['name']}, Phone: {u['phone']}, ID: {u['user_id']}")
        elif choice == "0":
            print("\n👋 Logged out from manager account.")
            break
        else:
            print("\n❌ Invalid option.")



# --- Main CLI Loop ---
def main():
    ensure_manager()
    while True:
        print("\n--- Welcome to DeliverySim ---")
        print("1. Sign In")
        print("2. Sign Up (Customer)")
        print("0. Exit")
        choice = input("Choose: ")
        if choice == "1":
            user = sign_in()
            if not user:
                continue
            if user["role"] == "customer":
                customer_menu(user)
            elif user["role"] == "courier":
                courier_menu(user)
            elif user["role"] == "manager":
                manager_menu()
        elif choice == "2":
            sign_up()
        elif choice == "0":
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid option.")

if __name__ == "__main__":
    main()
