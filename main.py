import json
import os
import uuid
from DispatchSystem import DispatchSystem
from Customer import Customer
from Courier import Courier
from Manager import Manager

from Order import Order

def load_orders_from_file(filename="orders.json"):
    orders = []
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            for entry in data:
                order = Order(
                    order_id=entry["order_id"],
                    customer_id=entry["customer_id"],
                    destination=entry["destination"]
                )
                order.status = entry["status"]
                orders.append(order)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return orders


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
    customer = Customer(user["user_id"], user["name"], user["address"], user["phone"])
    while True:
        print("\n--- Customer Menu ---")
        print("1. Create new order")
        print("2. View order history")
        print("3. View active orders")
        print("4. Track order status by ID")
        print("0. Logout")
        choice = input("Choose: ")
        if choice == "1":
            destination = input("Enter delivery destination: ")
            item = input("Enter item description: ")
            order = customer.create_order(destination, item)
    
    # 🧭 ננסה לשייך לפי מרחק בפועל עם Google Maps
            success = dispatch_system.assign_to_closest_courier_by_distance(order)

            if not success:
                print("⚠️ Order not created due to invalid location.")
                continue  # לא לשמור את ההזמנה

            dispatch_system.add_order_by_customer(order, customer.name, destination)
            dispatch_system.save_order_to_file(order)
            print(f"\n📦 Order created! ID: {order.order_id}")

        elif choice == "2":
            for order in dispatch_system.history_of_orders_by_customer(customer.customer_id):
                print(order)
        elif choice == "3":
            all_orders = load_orders_from_file()
            active_orders = customer.get_active_orders(all_orders)
            if not active_orders:
                print("\n📭 No active orders found.")
            else:
                print("\n📦 Active Orders:")
                for order in active_orders:
                    print(order)
        elif choice == "4":
            order_id = input("Enter your Order ID: ").strip()
            order_found = False
            for o in dispatch_system.orders:
                if o.order_id == order_id and o.customer_id == customer.customer_id:
                    print(f"\n📦 Order ID: {o.order_id}")
                    print(f"Destination: {o.destination}")
                    print(f"Item: {o.item_description}")
                    print(f"Status: {o.status}")
                    order_found = True
                    break
            if not order_found:
                print("❌ Order not found or doesn't belong to you.")

        elif choice == "0":
            print("\n👋 Logged out from customer account.")
            break
        else:
            print("\n❌ Invalid option.")



def courier_menu(user, dispatch_system):
    print(f"\n👋 Welcome {user['name']}!")

    courier_id = user.get("courier_id")
    region = user.get("region")
    courier = Courier(user["name"], courier_id, region)


    for order in dispatch_system.orders:
        if getattr(order, "courier_id", None) == courier.courier_id:
            courier.assign_order(order.order_id)


    courier = Courier(user["name"], courier_id, region)

    # טען את ההזמנות המשויכות
    for order in dispatch_system.orders:
        if order.courier and hasattr(order.courier, 'courier_id'):
            if order.courier.courier_id == courier.courier_id:
                courier.assign_order(order.order_id)

    while True:
        print("\n--- Courier Menu ---")
        print("1. View assigned deliveries")
        print("2. Update order status")
        print("0. Logout")
        courier_choice = input("Choose: ")

        if courier_choice == "1":
            if courier.deliveries:
                print("\n📦 Your Assigned Deliveries:")
                for oid in courier.deliveries:
                    for order in dispatch_system.orders:
                        if order.order_id == oid:
                            print(f"- Order ID: {order.order_id} | Destination: {order.destination} | Status: {order.status}")
            else:
                print("\nNo deliveries assigned.")

        elif courier_choice == "2":
            oid = input("Enter Order ID to update: ")
            found = False
            for order in dispatch_system.orders:
                if order.order_id == oid and order.courier and order.courier.courier_id == courier.courier_id:
                    print(f"Current status: {order.status}")
                    print("New status options: picked_up, in_transit, delivered, cancelled")
                    new_status = input("Enter new status: ").lower()
                    valid_transitions = {
                        "assigned": ["picked_up"],
                        "picked_up": ["in_transit"],
                        "in_transit": ["delivered"],
                    }

                    if new_status in ["picked_up", "in_transit", "delivered", "cancelled"]:
                        current = order.status
                        if new_status == "cancelled":
                            order.status = new_status
                            dispatch_system.save_orders_to_file()
                            print(f"🚫 Order {oid} cancelled.")
                        elif current in valid_transitions and new_status in valid_transitions[current]:
                            order.status = new_status
                            order.courier_id = courier.courier_id
                            dispatch_system.save_orders_to_file()
                            print(f"✅ Order {oid} status updated to {new_status}.")
                        else:
                            print(f"❌ Invalid status transition from {current} to {new_status}.")
                    else:
                        print("❌ Invalid status.")

                    found = True
                    break
            if not found:
                print("❌ Order not found or not assigned to you.")

        elif courier_choice == "0":
            break

        else:
            print("Invalid choice.")



def manager_menu():
    print("\n--- Manager Menu ---")
    manager = Manager("System Manager", dispatch_system)
    while True:
        print("\n1. View active orders")
        print("2. Auto-assign orders")
        print("3. Add new courier")
        print("4. View all couriers")
        print("6. View analytics summary")  # ← חדש
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
            region = input("Courier region: ")

            import uuid
            user_id = str(uuid.uuid4())[:8]
            courier_id = int(user_id[-3:], 16) % 1000

        # יצירת השליח כאובייקט
            new_courier = Courier(name, courier_id, region)
            dispatch_system.add_courier(new_courier)

    # הוספה גם ל-users.json עם courier_id
            user_data = {
                "name": name,
                "phone": phone,
                "password": password,
                "role": "courier",
                "user_id": user_id,
                "courier_id": courier_id,
                "region": region
            }

            try:
                with open("users.json", "r") as f:
                    users = json.load(f)
            except FileNotFoundError:
                users = []

            users.append(user_data)

            with open("users.json", "w") as f:
                json.dump(users, f, indent=4)

            print(f"Courier {name} added to region '{region}' with ID {courier_id}.")

        elif choice == "4":
            while True:
                print("\n--- Courier View Options ---")
                print("1. View all couriers")
                print("2. Filter couriers by region")
                print("3. View region load (number of orders per region)")
                print("0. Back to manager menu")
                sub_choice = input("Choose: ")

                if sub_choice == "1":
                    users = load_users()
                    print("\n--- All Couriers ---")
                    for u in users:
                        if u["role"] == "courier":
                            region = u.get("region", "Unknown")
                            print(f"Name: {u['name']}, Phone: {u['phone']}, ID: {u['user_id']}, Region: {region}")

                elif sub_choice == "2":
                    region_filter = input("Enter region name to filter: ").lower()
                    users = load_users()
                    print(f"\n--- Couriers in region '{region_filter}' ---")
                    found = False
                    for u in users:
                        if u["role"] == "courier" and u.get("region", "").lower() == region_filter:
                            print(f"Name: {u['name']}, Phone: {u['phone']}, ID: {u['user_id']}")
                            found = True
                    if not found:
                        print("⚠️ No couriers found in this region.")

                elif sub_choice == "3":
                    print("\n--- Region Load ---")
                    region_loads = dispatch_system.get_region_loads()
                    if region_loads:
                        for region, count in region_loads.items():
                            print(f"Region: {region} | Orders assigned: {count}")
                    else:
                        print("No assigned orders found.")

                elif sub_choice == "0":
                    break

                else:
                    print("❌ Invalid option.")
        elif choice == "6":
            print("\n📊 Analytics Summary:")
    
    # זמן משלוח ממוצע
            avg_time = dispatch_system.get_average_delivery_time()
            print(f"📦 Average Delivery Time: {avg_time:.2f} hours")

    # עומס לפי אזור
            print("\n🚚 Region Workload:")
            region_loads = dispatch_system.get_region_loads()
            for region, count in region_loads.items():
                print(f" - {region.title()}: {count} deliveries")

    # עומס לפי שליח
            print("\n👤 Courier Workload:")
            delivered_counts = dispatch_system.get_delivered_count_by_courier()
            for courier in dispatch_system.couriers:
                count = delivered_counts.get(courier.courier_id, 0)
                print(f" - {courier.name} (ID: {courier.courier_id}): {count} deliveries")

        elif choice == "0":
            break

        else:
            print("Invalid choice.")
        



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
                courier_menu(user, dispatch_system)
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
